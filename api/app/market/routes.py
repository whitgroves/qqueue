from flask import request
from flask.wrappers import Response

from app import db
from app.market import market
from app.market.models import Product
from app.utils.web import create_response


@market.route('/')
def get_market() -> Response:
    products = [p.to_dict() for p in db.session.query(Product).all()]
    # for p in db.session.query(Product).all():
    #     products.append(p.to_dict())

    return create_response(status=200, products=products)
