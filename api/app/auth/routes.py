from flask import jsonify, request
from flask.wrappers import Response
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from models import User
from app.auth import auth


@auth.route('/register', methods=['POST'])
def register() -> Response:
    error = 'Something went wrong.'
    
    try:
        error = 'Headers must include registration data.'
        email = request.json['email']
        password = request.json['password']

        error = 'An account is already registered to that email.'
        assert not _safe_get_user_by_email(email)

        error = 'There was an error while creating the account.'
        u = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(u)
        db.session.commit()

    except Exception as e:
        print(f'Exception encountered during registration: {e}')

        db.session.rollback()
        print('DB session rolled back successfully.')

        return _create_response(500, error)

    return _create_response(200, 'User registered successfully.')


@auth.route('/login', methods=['POST'])
def login() -> Response:
    error = 'Something went wrong.'

    try:
        error = 'Headers must include registration data.'
        email = request.json['email']
        password = request.json['password']

        error = 'That username/password pair was incorrect.'
        u = _safe_get_user_by_email(email)
        assert u
        assert check_password_hash(u.password_hash, password)

    except Exception as e:
        print(f'Exception encountered during login: {e}')

        db.session.rollback()
        print('DB session rolled back successfully.')

        return _create_response(500, error)

    return _create_response(200, 'User logged in successfully.')


def _safe_get_user_by_email(email:str) -> User:
    """
    Attempts to retrieve a user account with an email matching <email>.
    Exceptions fail silently and are printed to the console.

    Args:
        email (str): The email of the desired account.

    Returns:
        User: A database model of the user account. 
            Returns None if no match is found.
    """
    try:
        return db.session.query(User).filter_by(email=email).one()
    except Exception as e:
        print(f'Failed fetch from database produced this error: {e}')
        None

def _create_response(status:int, message:str) -> Response:
    """
    Creates a JSON-like response to send back to the client.

    Args:
        status (int): The HTTP status of the response.
        message (str): A message to return to the client.

    Returns:
        Response: A JSON object containing both <status> and <message>.
    """
    return jsonify({
        'status': status,
        'request': message
    })
    
