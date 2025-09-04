from flask import Blueprint

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/', methods=["GET"])
def test():
    return "hello world";

