from flask import Blueprint, jsonify, request
from models import Repo, AllowedIP
from marshmallow import ValidationError
from schema import ReposResponseSchema ,ReposWithIpResponseSchema, IpsResponseSchema, CrudIpRequestSchema, CrudIpResponseSchema
from __init__ import db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/repos", methods=["GET"])
def get_repos():
    repos = Repo.query.all()
    schema = ReposResponseSchema();
    response = schema.dump({"repos": repos})
    return jsonify(response), 200

@admin_bp.route("/repos-with-ips", methods=["GET"])
def get_repos_with_ips():
    repos = Repo.query.all()
    schema = ReposWithIpResponseSchema()
    response = schema.dump({"repos" : repos})
    return jsonify(response), 200

@admin_bp.route("/repos/<int:id>/ips", methods=["GET"])
def get_ips(id):
    ips = AllowedIP.query.filter_by(repo_id=id).all()
    schema = IpsResponseSchema()
    response = schema.dump({"ips": ips})
    return jsonify(response), 200


@admin_bp.route("/repos/<int:id>/ips", methods=["POST"])
def add_ip(id):
    data = request.get_json()
    request_schema = CrudIpRequestSchema()
    response_schema = CrudIpResponseSchema()

    try:
        validated =request_schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    repo = Repo.query.get(id)
    if not repo:
        return jsonify({"error": "Repo not found"}), 404

    
    new_ip = AllowedIP(ip_address=validated["ip_address"], repo_id=id)
    db.session.add(new_ip)
    db.session.commit()

    return jsonify(response_schema.dump({
        "message": "IP added successfully",
        "repo_id": id,
        "ip": validated["ip_address"]
    })), 201


@admin_bp.route("/repos/<int:id>/ips/<int:ip_id>", methods=["PUT"])
def update_ip(id, ip_id):

    data = request.get_json()
    request_schema = CrudIpRequestSchema()
    response_schema = CrudIpResponseSchema()

    try:
        validated = request_schema.load(data)
    except ValidationError as err:
        return jsonify({"error" : err.messages})

    repo = Repo.query.get(id)
    if not repo:
        return jsonify({"error": "Repo not found"}), 404

    ip_entry = AllowedIP.query.filter_by(id=ip_id, repo_id=id).first()
    if not ip_entry:
        return jsonify({"error": "IP address not found"}), 404


    ip_entry.ip_address = validated["ip_address"]
    db.session.commit()

    return jsonify(response_schema.dump({
        "message": "IP updated successfully",
        "repo_id": id,
        "ip": validated["ip_address"]
    })), 200


@admin_bp.route("/repos/<int:id>/ips/<int:ip_id>", methods=["DELETE"])
def delete_ip(id, ip_id):

    response_schema = CrudIpResponseSchema()

    repo = Repo.query.get(id)
    if not repo:
        return jsonify({"error": "Repo not found"}), 404

    ip_entry = AllowedIP.query.filter_by(id=ip_id, repo_id=id).first()
    if not ip_entry:
        return jsonify({"error": "IP address not found"}), 404

    db.session.delete(ip_entry)
    db.session.commit()

    return jsonify(response_schema.load({
        "message": "IP deleted successfully",
        "repo_id": id,
        "ip":  ip_entry.ip_address
    })), 200

