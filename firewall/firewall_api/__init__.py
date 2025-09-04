from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 
from dotenv import load_dotenv
db = SQLAlchemy()
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] =  DATABASE_URL
    db.init_app(app)
    
    from routes.users import users_bp
    from routes.admin import admin_bp

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        from models import Repo, AllowedIP  
        db.create_all()

    return app
