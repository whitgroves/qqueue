# import functools
from flask import jsonify, request
from flask.blueprints import Blueprint
# from werkzeug.security import generate_password_hash, check_password_hash

# from app import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    return jsonify({
        'status': 200,
        'request': request.json
    })
