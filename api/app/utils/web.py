from decimal import Decimal
from flask import jsonify
from flask.json import JSONEncoder
from flask.wrappers import Response

dev_token = 'halfbaked'


def json_response(status: int, **kwargs: dict) -> Response:
    """
    A little hack to make populating API responses easier.

    Returns:
        Response: A JSON Response containing <status> and <kwargs> as key-value pairs.
    """
    kwargs['status'] = status
    return jsonify(kwargs)


class DecimalEncoder(JSONEncoder):
    """
    An encoder class to serialize price data since it is stored as a Decimal under the hood 
    and cannot be serialized to JSON out of the box. Overrides <JSONEncoder.default>.
    """
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return JSONEncoder.default(self, obj)