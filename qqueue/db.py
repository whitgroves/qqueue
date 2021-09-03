import sqlite3
import click
from flask import current_app, g  # special objects to access app and db
from flask import Flask  # included for documentation
from flask.cli import with_appcontext

SCHEMA_FILE = 'schema.sql'

def get_db():
    """
    Connects to the database defined in the app config.
    Connection is stored in g.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row  # returns dict-like rows
   
    print(type(g.db))  # for docs
    return g.db

def close_db(e=None):
    """
    Closes the database stored in g, if there is one.
    """
    # for docs
    if e is not None:
        print(type(e))
    
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """
    Implementation of init_db_command().
    Drops and re-creates the database per <SCHEMA_FILE>.
    """
    db = get_db()
    with current_app.open_resource(SCHEMA_FILE) as schema_file:
        db.executescript(schema_file.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Command line command to drop existing data and create new tables.
    """
    init_db()
    click.echo('Database initialized.')

def init_app(app:Flask):
    """
    Registers close_db() and init_db_command() with <app>.
    Must be called from the factory on app creation.
    """
    app.teardown_appcontext(close_db)  # calls after returning a response
    app.cli.add_command(init_db_command)  # flask init-db