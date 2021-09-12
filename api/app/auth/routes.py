from flask import jsonify, request
from flask.wrappers import Response
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.auth import auth
from app.auth.models import User
from app.utils.web import json_response, dev_token


@auth.route('/', methods=['POST'])
def check_token() -> Response:
    error = 'Something went wrong.'

    try:
        error = 'Invalid token.'
        assert request.json['token'] == dev_token

        error = 'Request must include user data.'
        user_id = request.json['id']

        error = 'Could not retrieve user information.'
        user = db.session.query(User).get(int(user_id))
        
    except Exception as e:
        print(
            f'Exception encountered while checking token: {e} -> {error} -> {request.json}'
        )

        db.session.rollback()
        print('DB session rolled back successfully.')

        return json_response(500, error=error)

    return json_response(200,
                         message='User authenticated with server.',
                         user=user.to_dict(),
                         token=dev_token)


@auth.route('/register', methods=['POST'])
def register() -> Response:
    error = 'Something went wrong.'

    try:
        error = 'Request must include registration data.'
        email = request.json['email']
        password = request.json['password']

        error = 'An account is already registered to that email.'
        assert not _safe_get_user_by_email(email)

        error = 'There was an error while creating the account.'
        user = User(email=email,
                    password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    except Exception as e:
        print(
            f'Exception encountered during registration: {e} -> {error} -> {request.json}'
        )

        db.session.rollback()
        print('DB session rolled back successfully.')

        return json_response(500, error=error)

    return json_response(200,
                         message='User registered successfully.',
                         user=user.to_dict(),
                         token=dev_token)


@auth.route('/login', methods=['POST'])
def login() -> Response:
    error = 'Something went wrong.'

    try:
        error = 'Request must include login data.'
        email = request.json['email']
        password = request.json['password']

        error = 'That username/password pair was incorrect.'
        user = _safe_get_user_by_email(email)
        assert user
        assert check_password_hash(user.password_hash, password)

    except Exception as e:
        print(f'Exception encountered during login: {e}')

        db.session.rollback()
        print('DB session rolled back successfully.')

        return json_response(500, error=error)

    return json_response(200,
                         message='User logged in successfully.',
                         user=user.to_dict(),
                         token=dev_token)


def _safe_get_user_by_email(email: str) -> User:
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
