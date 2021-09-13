from flask import request
from flask.wrappers import Response

from app import db
from app.products import products
from app.products.models import Product
from app.utils.web import json_response


@products.route('/')
def all() -> Response:
    products = [p.to_dict() for p in db.session.query(Product).all()]
    return json_response(200, products=products)


@products.route('/<int:id>')
def one(id: int) -> Response:
    error = 'Something went wrong.'

    try:
        error = f'Product with id {id} does not exist.'
        product = _safe_get_product_by_id(id)
        assert product

    except Exception as e:
        print(f'Exception encountered during login: {e}')

        db.session.rollback()
        print('DB session rolled back successfully.')

        return json_response(500, error=error)

    return json_response(200, product=product.to_dict())


@products.route('/sell', methods=['POST'])
def sell() -> Response:
    error = 'Something went wrong.'

    try:
        error = 'Request must include product data.'
        name = request.json['name']
        
        # not required
        detail = request.json['detail'] if 'detail' in request.json else ''  

        error = 'There was an error while listing the product.'
        product = Product(name=name, detail=detail)
        db.session.add(product)
        db.session.commit()
    except Exception as e:
        print(
            f'Exception encountered during product listing: {e} -> {error} -> {request.json}'
        )

        db.session.rollback()
        print('DB session rolled back successfully.')

        return json_response(500, error=error)

    return json_response(200, product=product.to_dict())


def _safe_get_product_by_id(id: int) -> Product:
    try:
        return db.session.query(Product).get(id)
    except Exception as e:
        print(f'Failed Product lookup produced this error: {e}')
        return None