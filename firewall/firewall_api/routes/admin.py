from flask import Blueprint, jsonify, request
from models import Repo, AllowedIP
from __init__ import db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/repos", methods=["GET"])
def get_repos():
    repos = Repo.query.all()
    repo_list = [{"id": repo.id, "name": repo.name} for repo in repos]
    return jsonify({"repos": repo_list}), 200

@admin_bp.route("/repos-with-ips", methods=["GET"])
def get_repos_with_ips():
    repos = Repo.query.all()
    repo_list = []
    for repo in repos:
        repo_list.append({
            "id": repo.id,
            "name": repo.name,
            "allowed_ips": [ip.ip_address for ip in repo.allowed_ips]
        })
    return jsonify({"repos": repo_list}), 200

@admin_bp.route("/repos/<int:id>/ips", methods=["GET"])
def get_ips(id):
    ips = AllowedIP.query.filter_by(repo_id=id).all()
    ip_list = [ip.ip_address for ip in ips]  
    return jsonify({"repo_id": id, "allowed_ips": ip_list}), 200


@admin_bp.route("/repos/<int:id>/ips", methods=["POST"])
def add_ip(id):
    data = request.get_json()
    ip_address = data.get("ip_address")  

    if not ip_address:
        return jsonify({"error": "IP address is required"}), 400

    repo = Repo.query.get(id)
    if not repo:
        return jsonify({"error": "Repo not found"}), 404

    
    new_ip = AllowedIP(ip_address=ip_address, repo_id=id)
    db.session.add(new_ip)
    db.session.commit()

    return jsonify({
        "message": "IP added successfully",
        "repo_id": id,
        "ip": ip_address
    }), 201


@admin_bp.route("/repos/<int:id>/ips/<int:ip_id>", methods=["PUT"])
def update_ip(id, ip_id):
    data = request.get_json()
    updated_ip = data.get("updated_ip")

    if not updated_ip:
        return jsonify({"error": "Updated IP required"}), 400

    repo = Repo.query.get(id)
    if not repo:
        return jsonify({"error": "Repo not found"}), 404

    ip_entry = AllowedIP.query.filter_by(id=ip_id, repo_id=id).first()
    if not ip_entry:
        return jsonify({"error": "IP address not found"}), 404


    ip_entry.ip_address = updated_ip
    db.session.commit()

    return jsonify({
        "message": "IP updated successfully",
        "repo_id": id,
        "ip_id": ip_id,
        "new_address": updated_ip
    }), 200


@admin_bp.route("/repos/<int:id>/ips/<int:ip_id>", methods=["DELETE"])
def delete_ip(id, ip_id):
    
    repo = Repo.query.get(id)
    if not repo:
        return jsonify({"error": "Repo not found"}), 404

    ip_address = AllowedIP.query.filter_by(id=ip_id, repo_id=id).first()
    if not ip_address:
        return jsonify({"error": "IP address not found"}), 404

    db.session.delete(ip_address)
    db.session.commit()

    return jsonify({
        "message": "IP deleted successfully",
        "repo_id": id,
        "ip_id": ip_id,
    }), 200

