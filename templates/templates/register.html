<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Register | MediCore HMS</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet"/>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700;800&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet"/>
  <style>
    :root { --blue: #1a6eb5; --blue-light: #e8f1fb; }
    * { box-sizing: border-box; }
    body {
      font-family: 'Nunito', sans-serif;
      min-height: 100vh; margin: 0;
      background: #f0f4fa;
      display: flex; align-items: center; justify-content: center;
      padding: 40px 16px;
    }
    .register-card {
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 8px 40px rgba(26,110,181,0.12);
      padding: 40px 44px;
      width: 100%; max-width: 520px;
    }
    .brand-row {
      display: flex; align-items: center; gap: 12px;
      margin-bottom: 28px;
    }
    .brand-icon {
      width: 48px; height: 48px;
      background: linear-gradient(135deg,#1a6eb5,#00b4d8);
      border-radius: 14px;
      display: flex; align-items: center; justify-content: center;
      color: #fff; font-size: 1.3rem;
    }
    .brand-row h5 {
      font-family: 'Playfair Display', serif;
      margin: 0; font-size: 1.2rem; color: #1e2a3a;
    }
    h2 { font-weight: 800; font-size: 1.7rem; color: #1e2a3a; margin-bottom: 4px; }
    h2 span { color: var(--blue); }
    .sub { color: #64748b; font-size: 0.9rem; margin-bottom: 28px; }

    .form-label { font-size: 0.84rem; font-weight: 700; color: #374151; margin-bottom: 5px; }
    .form-control {
      border-radius: 10px; border: 1.5px solid #e2e8f0;
      padding: 10px 14px; font-size: 0.92rem;
      font-family: 'Nunito', sans-serif;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .form-control:focus {
      border-color: var(--blue);
      box-shadow: 0 0 0 3px rgba(26,110,181,0.12);
    }
    .input-group-text {
      border-radius: 10px 0 0 10px;
      border: 1.5px solid #e2e8f0; border-right: none;
      background: #f8fafc; color: #94a3b8;
    }
    .input-group .form-control { border-radius: 0 10px 10px 0; }

    .btn-register {
      background: linear-gradient(135deg, var(--blue), #00b4d8);
      border: none; border-radius: 10px;
      color: #fff; font-weight: 700; font-size: 1rem;
      padding: 12px; width: 100%;
      transition: all 0.2s;
    }
    .btn-register:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(26,110,181,0.32);
      color: #fff;
    }
    .pwd-strength { height: 4px; border-radius: 4px; margin-top: 6px; transition: all 0.3s; background: #e2e8f0; }
    .pwd-strength.weak   { background: #ef4444; width: 33%; }
    .pwd-strength.medium { background: #f97316; width: 66%; }
    .pwd-strength.strong { background: #22c55e; width: 100%; }

    .alert { border-radius: 10px; border: none; font-weight: 600; font-size: 0.88rem; }
    .alert-danger  { background: #fee2e2; color: #b91c1c; }
    .alert-success { background: #dcfce7; color: #15803d; }
    .login-link { text-align: center; margin-top: 20px; font-size: 0.9rem; color: #64748b; }
    .login-link a { color: var(--blue); font-weight: 700; text-decoration: none; }
    .login-link a:hover { text-decoration: underline; }
    @media (max-width: 576px) { .register-card { padding: 28px 20px; } }
  </style>
</head>
<body>
<div class="register-card">
  <div class="brand-row">
    <div class="brand-icon"><i class="fa-solid fa-heart-pulse"></i></div>
    <h5>MediCore HMS</h5>
  </div>

  <h2>Create <span>Account</span></h2>
  <p class="sub">Register to access the Hospital Management System</p>

  {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
      {% for cat, msg in messages %}
        <div class="alert alert-{{ cat }} alert-dismissible fade show mb-3">
          <i class="fa-solid {% if cat=='success' %}fa-circle-check{% else %}fa-circle-exclamation{% endif %} me-2"></i>
          {{ msg }}
          <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
      {% endfor %}
    {% endif %}
  {% endwith %}

  <form method="POST" action="{{ url_for('register') }}">
    <div class="row g-3">
      <div class="col-md-6">
        <label class="form-label">Full Name *</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fa-solid fa-id-card"></i></span>
          <input type="text" name="full_name" class="form-control" placeholder="Dr. / Mr. / Ms." required>
        </div>
      </div>
      <div class="col-md-6">
        <label class="form-label">Username *</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fa-solid fa-user"></i></span>
          <input type="text" name="username" class="form-control" placeholder="Unique username" required>
        </div>
      </div>
      <div class="col-12">
        <label class="form-label">Email Address *</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fa-solid fa-envelope"></i></span>
          <input type="email" name="email" class="form-control" placeholder="you@hospital.com" required>
        </div>
      </div>
      <div class="col-md-6">
        <label class="form-label">Password *</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fa-solid fa-lock"></i></span>
          <input type="password" name="password" id="pwd" class="form-control" placeholder="Min 6 characters" required oninput="checkStrength(this.value)">
        </div>
        <div class="pwd-strength" id="strengthBar"></div>
        <div id="strengthText" style="font-size:0.75rem;color:#94a3b8;margin-top:3px;"></div>
      </div>
      <div class="col-md-6">
        <label class="form-label">Confirm Password *</label>
        <div class="input-group">
          <span class="input-group-text"><i class="fa-solid fa-lock"></i></span>
          <input type="password" name="confirm_password" id="cpwd" class="form-control" placeholder="Repeat password" required oninput="checkMatch()">
        </div>
        <div id="matchText" style="font-size:0.75rem;margin-top:3px;"></div>
      </div>
    </div>

    <div class="mt-4">
      <button type="submit" class="btn btn-register">
        <i class="fa-solid fa-user-plus me-2"></i>Create Account
      </button>
    </div>
  </form>

  <div class="login-link">
    Already have an account? <a href="{{ url_for('login') }}">Sign in</a>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<script>
  function checkStrength(val){
    const bar=document.getElementById('strengthBar');
    const txt=document.getElementById('strengthText');
    if(!val){bar.className='pwd-strength';txt.textContent='';return;}
    const strong = val.length>=8 && /[A-Z]/.test(val) && /[0-9]/.test(val);
    const medium = val.length>=6;
    if(strong){bar.className='pwd-strength strong';txt.textContent='Strong ✓';txt.style.color='#16a34a';}
    else if(medium){bar.className='pwd-strength medium';txt.textContent='Medium';txt.style.color='#ea580c';}
    else{bar.className='pwd-strength weak';txt.textContent='Too weak';txt.style.color='#dc2626';}
  }
  function checkMatch(){
    const p=document.getElementById('pwd').value;
    const c=document.getElementById('cpwd').value;
    const t=document.getElementById('matchText');
    if(!c){t.textContent='';return;}
    if(p===c){t.textContent='Passwords match ✓';t.style.color='#16a34a';}
    else{t.textContent='Passwords do not match';t.style.color='#dc2626';}
  }
</script>
</body>
</html>
