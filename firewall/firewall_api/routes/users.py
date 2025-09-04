from flask import Blueprint

users_bp = Blueprint('users_bp', __name__)

@users_bp.route('/', methods=["GET"])
def test():
    return "hello world";


# @app.route("/repos/<repo_name>")
# def get_repo_objects(repo_name):
#     objects = REPO_OBJECTS.get(repo_name)
#     if objects is None:
#         abort(404)
#     return jsonify(objects)