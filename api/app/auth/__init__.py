from flask import Blueprint
import models

auth = Blueprint('auth', __name__)

from . import routes  # it had to be this way
