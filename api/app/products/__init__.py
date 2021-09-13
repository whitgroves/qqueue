from flask import Blueprint
import models

products = Blueprint('products', __name__)

from . import routes
