from flask import Blueprint, request, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        if 'signup' in request.form:
            username = request.form.get('username_signup')
            password = request.form.get('password_signup')
            password_repeat = request.form.get('password_repeat')
            
            if password != password_repeat:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('auth.auth'))

            user = User.query.filter_by(username=username).first()
            if user:
                flash('Username already exists', 'danger')
                return redirect(url_for('auth.auth'))

            new_user = User(
                username=username,
                password=generate_password_hash(password, method='sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('main.profile'))

        elif 'signin' in request.form:
            username = request.form.get('username_signin')
            password = request.form.get('password_signin')
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('main.profile'))
            else:
                flash('Login unsuccessful. Please check username and password', 'danger')

    return render_template('auth.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
