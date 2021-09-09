import time
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

# Config

import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Database

db = SQLAlchemy(app)
migrate = Migrate(app, db)
import models  # depends on db

# Routes

@app.route(f'{config.Config.ROUTE_PREFIX}/time')
def get_current_time():
    return jsonify({'time': time.time()})

@app.route(f'{config.Config.ROUTE_PREFIX}/products')
def get_all_products():
    return jsonify({'products': _get_all_products()})

@app.route(f'{config.Config.ROUTE_PREFIX}/products/<int:id>')
def get_single_product(id:int):
    return jsonify({'product': _mock_product(product_id=id)})

@app.route(f'{config.Config.ROUTE_PREFIX}/login', methods=['POST'])
@cross_origin()
def login():
    is_vendor = request.json['is_vendor']
    email = request.json['email']
    
    if _is_authenticated(request.json):
        id = request.json['id']
    else:

        if is_vendor:
            entity = _get_vendor_by_email(email)
        else:
            entity = _get_user_by_email(email)
    
        try:
            assert entity
            assert check_password_hash(entity.password_hash, request.json['password'])
        except AssertionError:
            return jsonify({
                'status': 500,
                'error': 'Username or password was incorrect.'
            })
            
        id = entity.id
        
    return jsonify({
        'status': 200,
        'email': email,
        'id': id,
        'is_vendor': is_vendor,
        'access_token': config.Config.DEV_ACCESS_TOKEN,  # TODO: actually generate this
        'refresh_token': config.Config.DEV_REFRESH_TOKEN
    })

@app.route(f'{config.Config.ROUTE_PREFIX}/logout')
def logout():
    # TODO: clear user's auth and refresh tokens.
    return jsonify({
        'status': 200
    })

@app.route(f'{config.Config.ROUTE_PREFIX}/register', methods=['POST'])
@cross_origin()
def register():
    is_vendor = request.json['is_vendor']
    email = request.json['email']
    pw_hash = generate_password_hash(request.json['password'])

    if is_vendor:
        lookup_fn = _get_vendor_by_email
        entity = models.Vendor(email=email, password_hash=pw_hash)
    else:
        lookup_fn = _get_user_by_email
        entity = models.User(email=email, password_hash=pw_hash)

    # check if email already exists
    try:
        assert not lookup_fn(email)
    except:
        return jsonify({
            'status': 500,
            'error': 'Email is already registered.'
        })
    
    try:
        db.session.add(entity)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 500,
            'error': e
        })
    
    return jsonify({
        'status': 200,
        'email': entity.email,
        'id': entity.id,
        'is_vendor': is_vendor,
        'access_token': config.Config.DEV_ACCESS_TOKEN,
        'refresh_token': config.Config.DEV_REFRESH_TOKEN
    })

@app.route(f'{config.Config.ROUTE_PREFIX}/store/<int:id>')
def get_vendor_store(id:int):
    return jsonify({
        'name': f'Vendor #{id}\'s store',
        'products': _get_products_by_vendor_id(id)
    })

# Helpers

def _mock_product(product_id:int) -> dict:
    vendor_id = product_id % 3 + 1
    return {
        'id': product_id,
        'name': f'Product #{product_id} by Vendor #{vendor_id}',
        'tagline': 'A fine product.',
        'image_url': 'https://via.placeholder.com/300',
        'image_thumbnail': 'https://via.placeholder.com/100',
        'website': 'https://github.com/whitgroves',
        'qty': 10,
        'price': 3.5,
        'vendor_id': vendor_id,
        'detail': 'Lorem ipsum, you all know the drill by now.\
                   Detail about the item goes here.'
    }

def _get_all_products(mock_vol=10) -> dict:
    products = []
    for i in range(mock_vol):
        product_id = i+1
        product = _mock_product(product_id=product_id)  
        products.append(product)

    return products 

def _get_user_by_email(email:str) -> models.User:
    try:
        return db.session.query(models.User).filter_by(email=email).one()
    except:
        return None

def _get_vendor_by_email(email:str) -> models.Vendor:
    try:
        return db.session.query(models.Vendor).filter_by(email=email).one()
    except:
        return None

def _get_products_by_vendor_id(vendor_id:int) -> list:
    try:
        products = _get_all_products()
        return [p for p in products if p['vendor_id'] == vendor_id]
        # return db.session.query(models.Product).filter_by(vendor_id=vendor_id)
    except:
        return None

def _is_authenticated(data:dict) -> bool:
    if 'access_token' in data:
        if data['access_token'] == config.Config.DEV_ACCESS_TOKEN:
            return True

    if 'refresh_token' in data:
        if data['refresh_token'] == config.Config.DEV_REFRESH_TOKEN:
            return True

    return False
