from flask import Blueprint, jsonify, flash, render_template, request, redirect, url_for, abort
from .models import Team, User, UserTeams, Message, Script
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.routing import BaseConverter
from . import db
from datetime import datetime, timedelta
import random, string
import deepl
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
views = Blueprint('views', __name__)
translator = deepl.Translator(os.environ["API_KEY1"])
genai.configure(api_key=os.environ["API_KEY"])

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
                return redirect(url_for('views.team_select'))
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
    if request.method=='POST':
        room_code = request.form.get('room_code')
        team  = Team.query.filter_by(team_code=room_code).first()

        joined_team = UserTeams.query.filter_by(user_id=current_user.user_id).all()
        team_ids = [ut.team_id for ut in joined_team]

        if team_ids:
            team_list = Team.query.filter(Team.team_id.in_(team_ids)).all()
        else:
            team_list = []

        if team:
            user_id = current_user.user_id
            existing_user_team = UserTeams.query.filter_by(team_id=team.team_id, user_id=user_id).first()
            if existing_user_team:
                return redirect(url_for('views.workspace', team_id=team.team_id))
            else:
                new_user_team = UserTeams(team_id = team.team_id, user_id=user_id)
                db.session.add(new_user_team)
                db.session.commit()
                return redirect(url_for('views.workspace', team_id=team.team_id))
        else:
            flash('Invalid team code.', 'danger')
            return render_template('team_select.html', team_list=team_list)

    joined_team = UserTeams.query.filter_by(user_id=current_user.user_id).all()
    team_ids = [ut.team_id for ut in joined_team]
    if team_ids:
        team_list = Team.query.filter(Team.team_id.in_(team_ids)).all()
    else:
        team_list = []

    return render_template('team_select.html', team_list=team_list)

@views.route('/workspace/<int:team_id>', methods=['GET', 'POST'])
@login_required
def workspace(team_id):

    check_valid_user = UserTeams.query.filter_by(team_id=team_id, user_id=current_user.user_id).first()

    if not check_valid_user:
        abort(403)

    team = Team.query.get_or_404(team_id)
    user_teams = UserTeams.query.filter_by(team_id=team_id).all()
    user_team_ids = [ut.user_team_id for ut in user_teams]  
    msgs = Message.query.filter(Message.user_team_id.in_(user_team_ids)).order_by(Message.created_at.asc()).all()
    if request.method == 'POST':

        message_content = request.form.get('message_content')
        if message_content:
            user_team = UserTeams.query.filter_by(team_id=team_id, user_id=current_user.user_id).first()
            if user_team:
                new_message = Message(content=message_content, user_team_id=user_team.user_team_id)
                db.session.add(new_message)
                db.session.commit()
                return jsonify({
                    'username': current_user.username,
                    'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'content': new_message.content
                })
        return jsonify({'error': 'Message content missing'}), 400 

    return render_template('workspace.html', team_name=team.team_name,team_code = team.team_code,  team_id=team_id, messages=msgs)

@views.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    target_lang = 'EN-US'

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return jsonify({'translatedText': result.text})
    except deepl.exceptions.AuthorizationException as e:
        return jsonify({'error': 'Authorization failed: ' + str(e)})
    except Exception as e:
        return jsonify({'error': str(e)})
    
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
            new_user_team = UserTeams(team_id= new_team_chat.team_id, user_id=current_user.user_id)
            db.session.add(new_user_team)
            db.session.commit()
            return redirect(url_for('views.workspace', team_id=new_team_chat.team_id))
        else:
            return redirect(url_for('views.team_select' ))
    return render_template('team_create.html')

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    
    if request.method == 'POST':
        name = request.form.get('name')
        dob = request.form.get('dob')
        email = request.form.get('email')
        username = request.form.get('username')
        
        if name:
            user.name = name
        if dob:
            user.dob = datetime.strptime(dob, '%Y-%m-%d')
        if email:
            user.email = email
        if username:
            user.username = username
        db.session.commit()
        return redirect(url_for('views.profile'))
    
    return render_template('profile.html', user=user)

@views.route('/suggest_emoji', methods=['POST'])
def suggest_emoji():
    data = request.json
    input_text = data.get('text', '')

    prompt = f"""
    Provide a list of 5 emojis that best represent the sentiment or key concepts of the following text. 
    Only return the emojis, without any additional text or explanation.

    Text: "{input_text}"
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    return jsonify({'emojis': response.text.strip()})