from flask import Blueprint, jsonify, flash, render_template, request, redirect, url_for
from .models import Team, User, UserTeams, Message, Script
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime, timedelta
import random

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('login.html')

@views.route('/authentication', methods=['GET', 'POST'])
def authentication():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            print(username)
            print(password)
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return render_template('base.html')
            else:
                flash('Invalid username or password.', 'danger')
                return redirect(url_for('views.authentication'))

        elif form_type == 'register':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            password1 = request.form.get('password1')
            if password == password1:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = User(username=username, email=email, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('views.authentication'))
    return render_template('login.html')
