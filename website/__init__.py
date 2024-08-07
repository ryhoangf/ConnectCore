from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'idont know'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:ryhoangf@localhost/connectcore'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        from . import models  
        db.create_all()
        
        from .views import views

        app.register_blueprint(views, url_prefix='/')
    return app
