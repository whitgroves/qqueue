import time
import os
from flask import Flask, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config:object=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        import config
        app.config.from_object(config.Config)
    else:
        app.config.from_object(test_config)

    # make sure the instance folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    # sanity check route
    @app.route('/api/time')
    def get_current_time() -> Response:
        return jsonify({'time': time.time()})
    
    from app.auth import auth
    app.register_blueprint(auth, url_prefix=f'/auth')

    db.init_app(app)
    migrate.init_app(app, db)

    return app
