from . import db
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(255))
    dob = db.Column(db.Date)
    password = db.Column(db.String(255), nullable=False)

class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

class TeamTask(db.Model):
    __tablename__ = 'teamtask'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)

class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)

class PersonalTask(db.Model):
    __tablename__ = 'personaltask'
    task_id = db.Column(db.Integer, db.ForeignKey('teamtask.task_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

class UserTeams(db.Model):
    __tablename__ = 'userteams'
    user_team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    role = db.Column(db.String(255))
    joined_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

class Badges(db.Model):
    __tablename__ = 'badges'
    badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

class UserBadges(db.Model):
    __tablename__ = 'userbadges'
    user_badges_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badges.badge_id'), nullable=False)
    awarded_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
