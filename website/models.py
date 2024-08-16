from . import db
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    team_code = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(255))
    dob = db.Column(db.Date)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.user_id)

    @property
    def is_active(self):
        return True
    
    @property
    def is_authenticated(self):
        return True
 
class Message(db.Model):
    __tablename__ = 'message'
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_team_id = db.Column(db.Integer, db.ForeignKey('userteams.user_team_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    user_team = db.relationship('UserTeams', backref='messages')

class Script(db.Model):
    __tablename__ = 'Script'
    script_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_team_id = db.Column(db.Integer, db.ForeignKey('userteams.user_team_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

class UserTeams(db.Model):
    __tablename__ = 'userteams'
    user_team_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    role = db.Column(db.String(255))
    joined_at = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)

    user = db.relationship('User', backref='user_teams')
    team = db.relationship('Team', backref='user_teams')
