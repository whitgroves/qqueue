import time
from flask import Flask, redirect, url_for, jsonify, request
from flask_login.utils import logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

# Config

import config

api = Flask(__name__)
api.config.from_object(config.Config)
# login = LoginManager(api)
# CORS(app)  # cross-origin support to enable local POST requests

# Database

db = SQLAlchemy(api)
migrate = Migrate(api, db)
import models  # depends on db and login

# Routes

@api.route(f'{config.Config.ROUTE_PREFIX}/time')
def get_current_time():
    return jsonify({'time': time.time()})

@api.route(f'{config.Config.ROUTE_PREFIX}/products')
def get_all_products():
    return jsonify(_get_all_products(mock_vol=6))

@api.route(f'{config.Config.ROUTE_PREFIX}/products/<int:id>')
def get_single_product(id:int):
    return jsonify({'product':_mock_product(id=id)})

@api.route(f'{config.Config.ROUTE_PREFIX}/login', methods=['POST'])
@cross_origin()
def login():
    if not _is_authenticated(request.json):
        try:
            user = _get_user_by_email(request.json['email'])
            assert user
            assert check_password_hash(
                user.password_hash, request.json['password']
            )
        except:
            return jsonify({
                'status': 500,
                'error': 'Username or password was incorrect.'
            })

        # login_user(user)  # has parameter to persist login ('remember me')
        
    return jsonify({
        'status': 200,
        'message': 'User is logged in.',
        'access_token': config.Config.DEV_ACCESS_TOKEN,
        'refresh_token': config.Config.DEV_REFRESH_TOKEN
    })

@api.route(f'{config.Config.ROUTE_PREFIX}/logout')
def logout():
    # logout_user()
    return jsonify({
        'status': 200,
        'message': f'User was logged out.'
    })

@api.route(f'{config.Config.ROUTE_PREFIX}/register', methods=['POST'])
@cross_origin()
def register():
    email = request.json['email']

    # check if email already exists
    try:
        assert not _get_user_by_email(email)
    except:
        return jsonify({
            'status': 500,
            'error': 'Email already registered.'
        })
    
    user = models.User(
        email=email, 
        password_hash=generate_password_hash(request.json['password'])
    )
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'error': e
        })
    
    return jsonify({
        'status': 200,
        'message': f'User {user.email} registered under id {user.id}',
        'access_token': config.Config.DEV_ACCESS_TOKEN,
        'refresh_token': config.Config.DEV_REFRESH_TOKEN
    })

# Helpers

def _mock_product(id:int) -> dict:
    """Returns a mocked instance of a product dict with id = <id>.

    Args:
        id (int): Sets the id of the mocked product.

    Returns:
        dict: A product dictionary with placeholder information.
    """
    return {
        'id': id,
        'name': f'Product #{id}',
        'tagline': 'A fine product.',
        'image_url': 'https://via.placeholder.com/300',
        'image_thumbnail': 'https://via.placeholder.com/100',
        'website': 'https://github.com/whitgroves',
        'qty': 10,
        'price': 3.5,
        'vendor_id': 0,
        'detail': 'Lorem ipsum, you all know the drill by now.\
                   Detail about the item goes here.'
    }

def _get_all_products(mock_vol=0) -> dict:
    """Fetches all products from the database. Will include mocked products
        if <mock_vol> is set.

    Args:
        mock_vol (int, optional): The number of mock products to include 
            in the list. Defaults to 5.

    Returns:
        dict: A JSON-like dictionary containing a list of product dictionaries.
    """
    products = []
    for i in range(mock_vol):
        product = _mock_product(id=i+1)  # product IDs start at 1.
        products.append(product)

    return {'products': products} 

def _get_user_by_email(email:str) -> models.User:
    try:
        return db.session.query(models.User).filter_by(email=email).one()
    except:
        return None

def _is_authenticated(data:dict) -> bool:
    """
    Determines whether data contains authentication or refresh tokens.
    Typically used with request.json.

    Args:
        data (dict): JSON-like data to check against.

    Returns:
        bool: Whether the data has a valid auth token.
    """
    if 'access_token' in data:
        if data['access_token'] == config.Config.DEV_ACCESS_TOKEN:
            return True

    if 'refresh_token' in data:
        if data['refresh_token'] == config.Config.DEV_REFRESH_TOKEN:
            return True

    return False
