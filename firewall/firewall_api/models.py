from flask_sqlalchemy import SQLAlchemy
from __init__ import db

class Repo(db.Model):
    __tablename__ = "repos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    allowed_ips = db.relationship("AllowedIP", backref="repo", cascade="all, delete-orphan")

class AllowedIP(db.Model):
    __tablename__ = "allowed_ips"

    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey("repos.id"), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
