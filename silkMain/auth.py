import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from silkMain.db import get_db

bp = Blueprint('auth', __name__, url_prefix = '/auth')

# views

# register
@bp.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required'
        elif not password:
            error = 'Password is required'
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (email, password) VALUES (?, ?)",
                    (email, generate_password_hash(password + email)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"This email is already in use"
            else:
                session.clear()
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')

# login
@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password+email):
            flash('Incorrect email and/or password')
        
        else:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
    return render_template('auth/login.html')

# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view

