from flask import Blueprint
from . import models

products = Blueprint('products', __name__)

from . import routes
