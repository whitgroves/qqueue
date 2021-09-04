import time
from flask import Flask

app = Flask(__name__)

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/products')
def get_all_products():
    products = []
    for i in range(50):
        id = i + 1
        product = {
            'id': id,
            'name': f'Product #{id}',
            'description': 'A fine product.',
            'image_url': '',
            'qty': 10,
            'price': f'${3.5:.02f}',
            'vendor_id': 0
        }
        products.append(product)

    return {'products': products} 