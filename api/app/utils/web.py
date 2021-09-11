from flask import json, jsonify
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