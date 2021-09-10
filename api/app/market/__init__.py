from flask import Blueprint
import models

market = Blueprint('market', __name__)

from . import routes
