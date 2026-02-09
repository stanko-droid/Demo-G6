from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from application.admin import admin_bp
from application.data.models.subscriber import Subscriber
# VIKTIGT: Vi importerar din nya Service här:
from application.services.auth_service import AuthService 

# --- INLOGGNINGSSIDAN ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # HÄR ANVÄNDER VI SERVICEN ISTÄLLET FÖR ATT GÖRA DET SJÄLVA
        user = AuthService.login(email, password)
        
        if user:
            login_user(user)
            return redirect(url_for('admin_bp.dashboard'))
        else:
            flash('Fel e-post eller lösenord.')

    return render_template('admin/login.html')

# --- LOGGA UT ---
@admin_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin_bp.login'))

# --- DASHBOARD ---
@admin_bp.route('/dashboard')
@login_required 
def dashboard():
    try:
        subscribers = Subscriber.query.all()
    except Exception as e:
        print(f"Kunde inte hämta prenumeranter: {e}")
        subscribers = []

    return render_template('admin/dashboard.html', subscribers=subscribers)