from logging import error
import time
from flask import Flask, json, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Config

import config

app = Flask(__name__)
app.config.from_object(config.Config)
# CORS(app)  # cross-origin support to enable local POST requests

db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models

# Routes

@app.route('/api/time')
def get_current_time():
    return jsonify({'time': time.time()})

@app.route('/api/products')
def get_all_products():
    return jsonify(_get_all_products(mock_vol=6))

@app.route('/api/products/<int:id>')
def get_single_product(id:int):
    return jsonify({'product':_mock_product(id=id)})

@app.route('/api/login', methods=['POST'])
@cross_origin()
def login():
    user = _get_user_by_email(request.json['email'])
    try:
        assert user
        assert check_password_hash(
            user.password_hash, request.json['password']
        )
    except Exception as e:
        return jsonify({
            'status': 500,
            'error': 'Username or password was incorrect.'
        })  
        
    return jsonify({
        'status': 200,
        'token': 'SUPER_SECRET',
        'message': f'User {user.email} logged in.'
    })


@app.route('/api/register', methods=['POST'])
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
            'message': f'User {user.email} registered under id {user.id}'
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