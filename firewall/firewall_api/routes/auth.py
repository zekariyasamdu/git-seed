from __init__ import db 
from models import AdminList
from flask import Blueprint, jsonify, request
from schema import LoginRequestSchema, LoginResponse
from marshmallow import ValidationError
from routes.admin import admin_bp
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from passlib.hash import sha256_crypt

@admin_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    request_schema = LoginRequestSchema()
    response_schema = LoginResponse()

    try:
        validated = request_schema.load(data)
    except ValidationError as err:
        return jsonify({"error" : err.messages}), 400

    admin_name = validated["admin_name"]
    password = validated["password"]
    
    admin_entry = AdminList.query.filter_by(admin_name = admin_name).first()
    if not admin_entry:
        return jsonify({"error" : "User not found"}), 404
    
    if admin_entry.password != password:
        return jsonify({"error" : "password incorrect"}), 401

    access_token = create_access_token(identity=admin_name)
    return jsonify(response_schema.dump({"access_token" : access_token, "token_type": "bearer", "user_id": admin_entry.id })), 200