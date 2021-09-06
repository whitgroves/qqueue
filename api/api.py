import time
from flask import Flask, request, redirect, url_for, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# CORS(app)  # cross-origin support to enable local POST requests

# Routes

@app.route('/api/time')
def get_current_time():
    return jsonify({'time': time.time()})

@app.route('/api/products')
def get_products():
    return jsonify(_get_all_products(mock_vol=6))

@app.route('/api/products/<int:id>')
def get_single_product(id:int):
    return jsonify({'product':_mock_product(id=id)})

@app.route('/api/login', methods=['POST'])
@cross_origin()
def post_products():
    email = request.json['email']
    password = request.json['password']
    if (email == 'test@test' and password == 'test'):
        return jsonify({'message':f'User {email} logged in.'})
    return jsonify({'error':'Username or password is incorrect.'})

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