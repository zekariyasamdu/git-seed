from app import app
from flask import Blueprint, request, jsonify, abort

# Middleware to check IP
@app.before_request
def check_ip():
    path = request.path
    client_ip = request.remote_addr
    
    if path.startswith("/repos/"):
        repo_name = path.split("/")[2] if len(path.split("/")) > 2 else None
        if not repo_name or repo_name not in REPO_ALLOWLIST:
            abort(404) 
        allowed_ips = REPO_ALLOWLIST[repo_name]
        if client_ip not in allowed_ips:
            abort(403) 
