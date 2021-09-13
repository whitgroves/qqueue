import os
import time
from flask import Flask, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection

db = SQLAlchemy()
migrate = Migrate()


@event.listens_for(Engine, 'connect')
def _set_sqlite_pragma(dbapi_connection, connection_record):
    """
    Listens for a SQLite 3 connection and turns on the database's FOREIGN KEY constraint.
    Must be explicitly set this way because SQLite does not enforce FK's by default.
    
    Reference:
        https://www.scrygroup.com/tutorial/2018-05-07/SQLite-foreign-keys/
    """
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute('PRAGMA foreign_keys=ON;')
        cursor.close()


def create_app(test_config: object = None) -> Flask:
    """
    Creates an instance of the app.

    Args:
        test_config (object, optional): A configuration class to use for test instances. Defaults to None.

    Returns:
        Flask: An instance of the API server.
    """
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
    app.register_blueprint(auth, url_prefix='/auth')

    from app.products import products
    app.register_blueprint(products, url_prefix='/products')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.utils.web import DecimalEncoder
    app.json_encoder = DecimalEncoder  # allows serialization of price data

    return app


app = create_app()  # declared here so SQLAlchemy/Alembic can pick up on custom models

if __name__ == '__main__':
    app.run()