from flask import Blueprint, request, jsonify, abort
from __init__ import db
# from dummy_data import Repo, AllowedIP

admin_bp = Blueprint("admin", __name__)

# ---------------- READ ----------------
@admin_bp.route("/repos/<string:repo_name>/ips", methods=["GET"])
def get_ips(repo_name):
    repo = Repo.query.filter_by(name=repo_name).first()
    if not repo:
        abort(404, "Repo not found")

    return jsonify([ip.ip_address for ip in repo.allowed_ips])

# ---------------- CREATE ----------------
@admin_bp.route("/repos/<string:repo_name>/ips", methods=["POST"])
def add_ip(repo_name):
    data = request.get_json()
    ip_address = data.get("ip")

    if not ip_address:
        abort(400, "IP address required")

    repo = Repo.query.filter_by(name=repo_name).first()
    if not repo:
        repo = Repo(name=repo_name)
        db.session.add(repo)
        db.session.commit()

    new_ip = AllowedIP(repo_id=repo.id, ip_address=ip_address)
    db.session.add(new_ip)
    db.session.commit()

    return jsonify({"message": f"IP {ip_address} added to {repo_name}"}), 201

# ---------------- UPDATE ----------------
@admin_bp.route("/repos/<string:repo_name>/ips/<int:ip_id>", methods=["PUT"])
def update_ip(repo_name, ip_id):
    data = request.get_json()
    new_ip = data.get("ip")

    if not new_ip:
        abort(400, "New IP required")

    repo = Repo.query.filter_by(name=repo_name).first()
    if not repo:
        abort(404, "Repo not found")

    ip_entry = AllowedIP.query.filter_by(id=ip_id, repo_id=repo.id).first()
    if not ip_entry:
        abort(404, "IP entry not found")

    ip_entry.ip_address = new_ip
    db.session.commit()

    return jsonify({"message": f"IP {ip_id} updated to {new_ip}"}), 200

# ---------------- DELETE ----------------
@admin_bp.route("/repos/<string:repo_name>/ips/<int:ip_id>", methods=["DELETE"])
def delete_ip(repo_name, ip_id):
    repo = Repo.query.filter_by(name=repo_name).first()
    if not repo:
        abort(404, "Repo not found")

    ip_entry = AllowedIP.query.filter_by(id=ip_id, repo_id=repo.id).first()
    if not ip_entry:
        abort(404, "IP entry not found")

    db.session.delete(ip_entry)
    db.session.commit()

    return jsonify({"message": f"IP {ip_id} deleted from {repo_name}"}), 200
