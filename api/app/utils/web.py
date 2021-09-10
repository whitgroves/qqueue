from flask import json, jsonify
from flask.wrappers import Response


def create_response(**kwargs: dict) -> Response:
    """
    A little hack to make populating API responses easier.

    Returns:
        Response: A JSON response containing <kwargs> as key-value pairs.
    """
    return jsonify(kwargs)