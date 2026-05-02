from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from datetime import datetime, date
from functools import wraps
import hashlib

app = Flask(__name__)
app.secret_key = 'medicore_super_secret_key_2024_!@#'
DATABASE = 'hospital.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(('medicore_salt_2024' + password).encode()).hexdigest()

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        role TEXT DEFAULT 'staff',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, age INTEGER, gender TEXT, phone TEXT,
        email TEXT, address TEXT, blood_group TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, specialization TEXT, phone TEXT, email TEXT,
        consultation_fee REAL DEFAULT 500.0, available_days TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER, doctor_id INTEGER,
        appointment_datetime TEXT, status TEXT DEFAULT 'Scheduled', notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(patient_id) REFERENCES Patients(id),
        FOREIGN KEY(doctor_id) REFERENCES Doctors(id)
    )''')
    c.execute("SELECT COUNT(*) FROM Users")
    if c.fetchone()[0] == 0:
        c.execute('INSERT INTO Users (username,email,password,full_name,role) VALUES (?,?,?,?,?)',
                  ('admin','admin@medicore.com',hash_password('admin123'),'Administrator','admin'))
    c.execute("SELECT COUNT(*) FROM Doctors")
    if c.fetchone()[0] == 0:
        c.executemany('INSERT INTO Doctors (name,specialization,phone,email,consultation_fee,available_days) VALUES (?,?,?,?,?,?)', [
            ('Dr. Priya Sharma','Cardiology','9876543210','priya@hospital.com',1200.0,'Mon,Tue,Wed,Thu,Fri'),
            ('Dr. Arjun Mehta','Neurology','9876543211','arjun@hospital.com',1500.0,'Mon,Wed,Fri'),
            ('Dr. Sneha Patel','Orthopedics','9876543212','sneha@hospital.com',800.0,'Tue,Thu,Sat'),
            ('Dr. Rohan Verma','Pediatrics','9876543213','rohan@hospital.com',600.0,'Mon,Tue,Wed,Thu,Fri,Sat'),
        ])
    conn.commit()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# AUTH
@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM Users WHERE (username=? OR email=?) AND password=?',
            (username, username, hash_password(password))
        ).fetchone()
        conn.close()
        if user:
            session['user_id']   = user['id']
            session['username']  = user['username']
            session['full_name'] = user['full_name']
            session['role']      = user['role']
            flash(f"Welcome back, {user['full_name'] or user['username']}!", 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username  = request.form['username'].strip()
        email     = request.form['email'].strip()
        full_name = request.form['full_name'].strip()
        password  = request.form['password']
        confirm   = request.form['confirm_password']
        if password != confirm:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')
        conn = get_db()
        existing = conn.execute('SELECT id FROM Users WHERE username=? OR email=?',(username,email)).fetchone()
        if existing:
            flash('Username or email already taken.', 'danger')
            conn.close()
            return render_template('register.html')
        conn.execute('INSERT INTO Users (username,email,password,full_name,role) VALUES (?,?,?,?,?)',
                     (username,email,hash_password(password),full_name,'staff'))
        conn.commit()
        conn.close()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    name = session.get('full_name','User')
    session.clear()
    flash(f'Goodbye, {name}! You have been logged out.', 'info')
    return redirect(url_for('login'))

# DASHBOARD
@app.route('/')
@login_required
def dashboard():
    conn = get_db()
    total_patients      = conn.execute('SELECT COUNT(*) FROM Patients').fetchone()[0]
    total_doctors       = conn.execute('SELECT COUNT(*) FROM Doctors').fetchone()[0]
    today               = date.today().strftime('%Y-%m-%d')
    todays_appointments = conn.execute("SELECT COUNT(*) FROM Appointments WHERE appointment_datetime LIKE ?",(today+'%',)).fetchone()[0]
    total_appointments  = conn.execute('SELECT COUNT(*) FROM Appointments').fetchone()[0]
    recent_appointments = conn.execute('''SELECT a.id,p.name as patient_name,d.name as doctor_name,a.appointment_datetime,a.status
        FROM Appointments a JOIN Patients p ON a.patient_id=p.id JOIN Doctors d ON a.doctor_id=d.id
        ORDER BY a.created_at DESC LIMIT 5''').fetchall()
    conn.close()
    return render_template('dashboard.html',total_patients=total_patients,total_doctors=total_doctors,
        todays_appointments=todays_appointments,total_appointments=total_appointments,recent_appointments=recent_appointments)

# PATIENTS
@app.route('/patients')
@login_required
def patients():
    search=request.args.get('search',''); gender_filter=request.args.get('gender','')
    conn=get_db(); query='SELECT * FROM Patients WHERE 1=1'; params=[]
    if search:
        query+=' AND (name LIKE ? OR phone LIKE ? OR email LIKE ?)'; params.extend([f'%{search}%']*3)
    if gender_filter:
        query+=' AND gender=?'; params.append(gender_filter)
    patients=conn.execute(query+' ORDER BY created_at DESC',params).fetchall(); conn.close()
    return render_template('patients.html',patients=patients,search=search,gender_filter=gender_filter)

@app.route('/patients/add',methods=['GET','POST'])
@login_required
def add_patient():
    if request.method=='POST':
        conn=get_db()
        conn.execute('INSERT INTO Patients (name,age,gender,phone,email,address,blood_group) VALUES (?,?,?,?,?,?,?)',
            (request.form['name'],request.form['age'],request.form['gender'],request.form['phone'],
             request.form['email'],request.form['address'],request.form['blood_group']))
        conn.commit(); conn.close()
        flash('Patient registered successfully!','success')
        return redirect(url_for('patients'))
    return render_template('add_patient.html')

@app.route('/patients/delete/<int:pid>')
@login_required
def delete_patient(pid):
    conn=get_db(); conn.execute('DELETE FROM Patients WHERE id=?',(pid,)); conn.commit(); conn.close()
    flash('Patient record deleted.','warning'); return redirect(url_for('patients'))

# DOCTORS
@app.route('/doctors')
@login_required
def doctors():
    search=request.args.get('search',''); spec_filter=request.args.get('specialization','')
    conn=get_db(); query='SELECT * FROM Doctors WHERE 1=1'; params=[]
    if search:
        query+=' AND (name LIKE ? OR phone LIKE ?)'; params.extend([f'%{search}%']*2)
    if spec_filter:
        query+=' AND specialization=?'; params.append(spec_filter)
    doctors=conn.execute(query+' ORDER BY name',params).fetchall()
    specializations=conn.execute('SELECT DISTINCT specialization FROM Doctors ORDER BY specialization').fetchall()
    conn.close()
    return render_template('doctors.html',doctors=doctors,search=search,spec_filter=spec_filter,specializations=specializations)

@app.route('/doctors/add',methods=['GET','POST'])
@login_required
def add_doctor():
    if request.method=='POST':
        conn=get_db()
        conn.execute('INSERT INTO Doctors (name,specialization,phone,email,consultation_fee,available_days) VALUES (?,?,?,?,?,?)',
            (request.form['name'],request.form['specialization'],request.form['phone'],request.form['email'],
             request.form['consultation_fee'],','.join(request.form.getlist('available_days'))))
        conn.commit(); conn.close()
        flash('Doctor added successfully!','success'); return redirect(url_for('doctors'))
    return render_template('add_doctor.html')

@app.route('/doctors/delete/<int:did>')
@login_required
def delete_doctor(did):
    conn=get_db(); conn.execute('DELETE FROM Doctors WHERE id=?',(did,)); conn.commit(); conn.close()
    flash('Doctor record deleted.','warning'); return redirect(url_for('doctors'))

# APPOINTMENTS
@app.route('/appointments')
@login_required
def appointments():
    status_filter=request.args.get('status',''); conn=get_db()
    query='''SELECT a.id,p.name as patient_name,d.name as doctor_name,d.specialization,
                    a.appointment_datetime,a.status,a.notes,d.consultation_fee
             FROM Appointments a JOIN Patients p ON a.patient_id=p.id JOIN Doctors d ON a.doctor_id=d.id WHERE 1=1'''
    params=[]
    if status_filter:
        query+=' AND a.status=?'; params.append(status_filter)
    appointments=conn.execute(query+' ORDER BY a.appointment_datetime DESC',params).fetchall(); conn.close()
    return render_template('appointments.html',appointments=appointments,status_filter=status_filter)

@app.route('/appointments/add',methods=['GET','POST'])
@login_required
def add_appointment():
    conn=get_db()
    if request.method=='POST':
        patient_id=request.form['patient_id']; doctor_id=request.form['doctor_id']
        appt_dt=request.form['appointment_datetime']; notes=request.form['notes']
        existing=conn.execute('SELECT id FROM Appointments WHERE doctor_id=? AND appointment_datetime=? AND status!="Cancelled"',(doctor_id,appt_dt)).fetchone()
        if existing:
            flash('Doctor is already booked at this time! Please choose a different slot.','danger')
        else:
            conn.execute('INSERT INTO Appointments (patient_id,doctor_id,appointment_datetime,notes) VALUES (?,?,?,?)',(patient_id,doctor_id,appt_dt,notes))
            conn.commit(); flash('Appointment scheduled successfully!','success'); conn.close()
            return redirect(url_for('appointments'))
    patients=conn.execute('SELECT id,name FROM Patients ORDER BY name').fetchall()
    doctors=conn.execute('SELECT id,name,specialization FROM Doctors ORDER BY name').fetchall()
    conn.close()
    return render_template('add_appointment.html',patients=patients,doctors=doctors)

@app.route('/appointments/update_status/<int:aid>/<status>')
@login_required
def update_status(aid,status):
    conn=get_db(); conn.execute('UPDATE Appointments SET status=? WHERE id=?',(status,aid)); conn.commit(); conn.close()
    flash(f'Appointment status updated to {status}.','info'); return redirect(url_for('appointments'))

# BILLING
@app.route('/billing/<int:aid>')
@login_required
def get_bill(aid):
    conn=get_db()
    data=conn.execute('''SELECT a.id,p.name as patient_name,d.name as doctor_name,
        d.specialization,a.appointment_datetime,d.consultation_fee
        FROM Appointments a JOIN Patients p ON a.patient_id=p.id JOIN Doctors d ON a.doctor_id=d.id WHERE a.id=?''',(aid,)).fetchone()
    conn.close()
    if not data: return jsonify({'error':'Not found'}),404
    fee=data['consultation_fee']; tax=round(fee*0.18,2); total=round(fee+tax,2)
    return jsonify({'appointment_id':data['id'],'patient_name':data['patient_name'],
        'doctor_name':data['doctor_name'],'specialization':data['specialization'],
        'appointment_datetime':data['appointment_datetime'],'consultation_fee':fee,'tax_18':tax,'total':total})

if __name__=='__main__':
    init_db()
    app.run(debug=True)
