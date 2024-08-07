from flask import Blueprint, jsonify, flash, render_template, request, redirect, url_for
from .models import Team, User, UserBadges, UserTeams, Message, Task, TeamTask, PersonalTask, Badges
from flask_login import login_required, current_user
from . import db
from datetime import datetime, timedelta
import random

views = Blueprint('views', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    return app

@views.route('/')
def home():
    return render_template('base.html')