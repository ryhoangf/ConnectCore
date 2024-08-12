from flask import Blueprint, jsonify, flash, render_template, request, redirect, url_for
from .models import Team, User, UserTeams, Message, Script
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.routing import BaseConverter
from . import db
from datetime import datetime, timedelta
import random, string

views = Blueprint('views', __name__)

length = 10;
def gen_team_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Login successful!', 'success')
                return render_template ('team_select.html')
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


@views.route('/team_select', methods=['GET','POST'])
@login_required
def team_select():
    room_code = request.form.get('room_code')
    team  = Team.query.filter_by(team_code=room_code).first()

    if team:
        user_id = current_user.user_id
        new_user_team = UserTeams(team_id = team.team_id, user_id=user_id)
        db.session.add(new_user_team)
        db.session.commit()
        return redirect(url_for('views.workspace', team_id=team.team_id))
    else:
        flash('Invalid team code.', 'danger')
        return render_template('team_select.html')
    return render_template('team_select.html')

@views.route('/workspace/<int:team_id>', methods=['GET', 'POST'])
@login_required
def workspace(team_id):
    team = Team.query.get_or_404(team_id)
    user_teams = UserTeams.query.filter_by(team_id=team_id).all()
    user_team_ids = [ut.user_team_id for ut in user_teams]  
    msgs = Message.query.filter(Message.user_team_id.in_(user_team_ids)).order_by(Message.created_at.asc()).all()
    if request.method == 'POST':
        message_content = request.form.get('message_content')
        if message_content:
            new_message = Message(content=message_content, user_team_id=user_teams.user_team_id, user_id=current_user.user_id)
            db.session.add(new_message)
            db.session.commit()
        return redirect(url_for('views.workspace', team_id=team_id))
    return render_template('workspace.html', team_name=team.team_name,team_code = team.team_code, team_id=team_id, messages=msgs)

@views.route('/team_create', methods=['GET','POST'])
@login_required
def team_create():
    if request.method == 'POST':
        team_name = request.form.get('name')
        if team_name:
            team_code = gen_team_code()
            new_team_chat = Team(team_name=team_name,team_code =team_code)
            db.session.add(new_team_chat)
            db.session.commit()
            return redirect(url_for('views.workspace', team_id=new_team_chat.team_id))
        else:
            return render_template('team_create.html')
    return render_template('team_create.html')

def send_message(team_id):
    if request.method == 'POST':
        message_content = request.form.get('message_content')
        if message_content:
            new_message = Message(content=message_content, team_id=team_id, user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
    return redirect(url_for('views.workspace', team_id=team_id))
