import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from flask.wrappers import Response
from werkzeug.security import check_password_hash, generate_password_hash
from qqueue.db import get_db


# Base route for authentication. (domain.com/auth/endpoint)
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Routes

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO user (email, pw_hash) VALUES (?, ?)',
                    (email, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f'User with email {email} is already registered.'
            else:
                return redirect(url_for('auth.login'))
        
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None

        user = _get_user('email', email)

        if user is None or not check_password_hash(user['pw_hash'], password):
            error = 'Username or password is incorrect.'

        if error is None:
            session.clear()  # cleanup old session
            session['user_id'] = user['id']  # set cookie
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# always runs before the view function, regardless of endpoint
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = _get_user('id', user_id)

# decorator to wrap the view so logins are required
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view

# Helpers

def _get_user(column:str, value:str):
    """
    Fetches a user from the database where column <column> has value <value>.
    Returns the first row found if there are multiple matches.
    Params:
        column: The database column to check against for a match.
        value:  The value to check for a match on.
    """
    query = f'SELECT * FROM user WHERE {column} = ?'
    return get_db().execute(query, (value, )).fetchone()
