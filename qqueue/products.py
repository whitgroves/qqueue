from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from qqueue.auth import login_required
from qqueue.db import get_db

bp = Blueprint('products', __name__)

# Routes

@bp.route('/')
def index():
    products = get_db().execute('SELECT * FROM product').fetchall()
    return render_template('products/index.html', products=products)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        title = request.form['title']
        detail = request.form['detail']
        error = None

        if not title:
            error = 'Title required.'
        
        if not detail:
            error = 'Detail required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (title, detail) VALUES (?, ?)',
                (title, detail)
            )
            db.commit()
            return redirect(url_for('products.index'))
    
    return render_template('products/add.html')

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id:int):
    product = get_product(id)

    if request.method == 'POST':
        title = request.form['title']
        detail = request.form['detail']
        error = None

        if not title:
            error = 'Title required.'
        
        if not detail:
            error = 'Detail required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE product SET title = ?, detail = ? WHERE id = ?',
                (title, detail, id)
            )
            db.commit()
            return redirect(url_for('products.index'))
    
    return render_template('products/update.html', product=product)

@bp.route('/<int:id>/delete', methods=('POST', ))
@login_required
def delete(id:int):
    assert get_product(id) is not None
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id, ))
    db.commit()
    return redirect(url_for('products.index'))

# Helpers

def get_product(id:int):
    product = get_db().execute(
        'SELECT * FROM product WHERE id = ?',
        (id, )
    ).fetchone()

    if product is None:
        abort(404, f'Product with id {id} does not exist.')

    # if check_login and not g.user:
    #     abort(403)

    return product