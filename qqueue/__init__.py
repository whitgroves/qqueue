import os
from flask import Flask

DEFAULT_CONFIG = 'config.py'
APP_DB = 'qqueue.sqlite'

def create_app(config=None) -> Flask:
    """
    Factory function to create and configure the app. By default,
    configuration values will be loaded from the <DEFAULT_CONFIG> file.
    Params:
        config: (?) A configuration mapping for the app.
                    Replaces <DEFAULT_CONFIG> if used.
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # replace with a random value when deploying.
        DATABASE=os.path.join(app.instance_path, APP_DB)
    )

    if config is None:
        # Will fail silently if <DEFAULT_CONFIG> does not exist.
        app.config.from_pyfile(DEFAULT_CONFIG, silent=True)
    else:
        print(type(config))  # for documentation purposes
        app.config.from_mapping(config)
    
    # Flask does not create the instance_path automatically.
    # We need this directory setup to house our db.
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # Sanity check that app is working.
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    # Connect to the database. Use "flask init-db" for first-time setup.
    from . import db
    db.init_app(app)

    # Setup the authentication routes.
    from . import auth
    app.register_blueprint(auth.bp)

    # Setup product listings.
    from . import products
    app.register_blueprint(products.bp)
    app.add_url_rule('/', endpoint='index')  # routes to products.index

    return app
