from flask import request
from flask.wrappers import Response

from app import db
from app.market import market
from app.market.models import Product
from app.utils.web import json_response


@market.route('/')
@market.route('/buy')
def buy() -> Response:
    products = [p.to_dict() for p in db.session.query(Product).all()]
    return json_response(200, products=products)

@market.route('/sell', methods=['POST'])
def sell() -> Response:
    error = 'Something went wrong.'
    
    try:
        error = 'Request must include product data.'
        name = request.json['name']
        detail = request.json['detail']
        
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
