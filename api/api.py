import time
from flask import Flask

app = Flask(__name__)


# Routes


@app.route('/api/time')
def get_current_time() -> dict:
    """Gets the current time.

    Returns:
        dict: The number of seconds since epoch.
    """
    return {'time': time.time()}


@app.route('/api/products')
def get_all_products() -> dict:
    """Fetches all products from the database. Data is not paginated.

    Returns:
        dict: A JSON-like dict with the following structure:
            'products': [
                {
                    'id': <int>,
                    ...
                },
                { ... },
                { ... }
            ]
    """
    products = []
    for i in range(50):
        product = _mock_product(id=i+1)
        products.append(product)

    return {'products': products} 


@app.route('/api/products/<int:id>')
def get_single_product(id:int) -> dict:
    """Fetches a single product by its <id>.

    Args:
        id (int): The id of the product to get.

    Returns:
        dict: A JSON-like dict with the following structure:
            {
                'id': <int>,
                'name': <str>,
                'tagline': <str>,
                'image_url': <str>,
                'image_thumbnail': <str>,
                'website': <str>
                'qty': <int>,
                'price': <str>,  # stored as an <int> in db.
                'vendor_id': <int>,
                'detail': <str>
            }
    """
    return {'product': _mock_product(id=id)}


# Helpers

def _mock_product(id:int) -> dict:
    return {
        'id': id,
        'name': f'Product #{id}',
        'tagline': 'A fine product.',
        'image_url': 'https://via.placeholder.com/300',
        'image_thumbnail': 'https://via.placeholder.com/100',
        'website': 'https://github.com/whitgroves',
        'qty': 10,
        'price': f'${3.5:.02f}',
        'vendor_id': 0,
        'detail': 'Lorem ipsum, you all know the drill by now.\
                   Detail about the item goes here.'
    }