import os
basedir = os.path.abspath(os.path.dirname(__file__))

class TestConfig(object):
    TESTING = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('QQ_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'qqtest.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config(object):
    """
    A configuration object to store Flask settings. Use with
    Flask().config.from_object() to apply to your Flask app.

    Config keys must be in all caps for Flask to load them.
    See https://flask.palletsprojects.com/en/2.0.x/config/#configuring-from-python-files.

    Additional keys can be added and used as needed in your app's
    custom logic.

    This class should not be instantiated.
    """

    SECRET_KEY = os.environ.get('QQ_SECRET_KEY') or 'oiwnf0ns09v4n#law3'

    ROUTE_PREFIX = os.environ.get('QQ_ROUTE_PREFIX') or '/api'

    # Database

    SQLALCHEMY_DATABASE_URI = os.environ.get('QQ_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'qqueue.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Dev Mocks

    DEV_ACCESS_TOKEN = 'j0gg#ly32*f2mc!3z'

    DEV_REFRESH_TOKEN = '09oi2nI#^!_v0af9p'