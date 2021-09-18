from flask import request
from flask.wrappers import Response
from flask_cors import cross_origin

from app import db
from app.products import products
from app.products.models import Product
from app.utils.web import json_response


@products.route('/')
@cross_origin()
def all() -> Response:
    products = [
        p.to_dict() for p in db.session.query(Product).all() if p.is_active
    ]
    return json_response(200, products=products)


@products.route('/<int:id>')
def one(id: int) -> Response:
    error = 'Something went wrong.'

    try:
        error = f'Product with id {id} does not exist.'
        product = _safe_get_product_by_id(id)
        assert product

    except Exception as e:
        print(f'Exception encountered while fetching a product: {e}')

        db.session.rollback()
        print('DB session rolled back successfully.')

        return json_response(500, error=error)

    return json_response(200, product=product.to_dict())


@products.route('/sell', methods=['POST'])
def sell() -> Response:
    error = 'Something went wrong.'

    try:
        # required fields
        error = 'Request must include product name.'
        name = request.json['name']

        error = 'Request must include product price.'
        price = request.json['price']

        error = 'Request must include seller id.'
        seller_id = request.json['seller_id']

        # not required
        detail = request.json['detail'] if 'detail' in request.json else ''
        tagline = request.json['tagline'] if 'tagline' in request.json else ''
        image_url = request.json[
            'image_url'] if 'image_url' in request.json else ''
        price = request.json['price'] if 'price' in request.json else 0

        error = 'There was an error while listing the product.'
        product = Product(name=name,
                          detail=detail,
                          tagline=tagline,
                          image_url=image_url,
                          price=price,
                          seller_id=seller_id,
                          is_active=True)
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


@products.route('/deactivate/<int:id>', methods=['POST'])
def deactivate(id: int) -> Response:
    error = 'Something went wrong.'

    try:
        error = 'Request must include user id.'
        user_id = request.json['user_id']

        error = 'Could not retrieve product with that id.'
        product = _safe_get_product_by_id(id)
        assert product

        error = 'User does not have permission to change that product.'
        assert product.seller_id == user_id

        error = 'Product is already inactive.'
        assert product.is_active

        error = 'There was an error while delisting the product.'
        product.is_active = False
        db.session.commit()
    except Exception as e:
        print(
            f'Exception encountered during product deactivation: {e} -> {error} -> {request.json}'
        )

        db.session.rollback()
        print('DB session rolled back successfully.')

        return json_response(500, error=error)

    return json_response(200)


def _safe_get_product_by_id(id: int) -> Product:
    try:
        product = db.session.query(Product).get(id)
        assert product.is_active
        return product
    except Exception as e:
        print(f'Product lookup failed with this error: {e}')
        return None