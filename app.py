from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,upgrade
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////opt/data/pft.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)


    app.config["SECRET_KEY"] = "supersecretkey123"  # change this in production
   
    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(uid)
    
    bcrypt = Bcrypt(app)

    from  route import register_routes
    register_routes(app, db,bcrypt)
    Migrate(app, db)

    def run_migrations():
        upgrade()

    return app


app = create_app()