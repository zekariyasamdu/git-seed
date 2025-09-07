from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os 
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
db = SQLAlchemy()
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY') 

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] =  DATABASE_URL
    app.config['JWT_SECRET_KEY'] = SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    jwt = JWTManager(app)
    db.init_app(app)

    from routes.admin import admin_bp

    app.register_blueprint(admin_bp)

    with app.app_context():
        from models import Repo, AllowedIP  
        db.create_all()

    return app
