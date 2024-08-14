from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO, send

db = SQLAlchemy()
login_manager=LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'idont know'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ryhoangf@localhost/connectcore'
    app.config['DEBUG']= True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import models  
        db.create_all()
        
        from .views import views
        app.register_blueprint(views, url_prefix='/')


        from .models import User
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
    return app
