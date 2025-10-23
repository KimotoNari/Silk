from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from silkMain.auth import login_required
from silkMain.db import get_db

bp = Blueprint('note', __name__)

def get_note(id, check_author=True):
    note = get_db().execute(
        'SELECT p.id, title, body, created, owner_id, username'
        ' FROM note p JOIN user u ON p.owner_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if note is None:
        abort(404, f"Note id {id} doesn't exist.")

    if check_author and note['owner_id'] !=g.user['id']:
        abort(403)

    return note

# views

@bp.route('/')
def index():
    db = get_db()
    notes = db.execute(
        'SELECT n.id, title, body, created, owner_id, username'
        ' FROM note n JOIN user u ON n.owner_id = u.id'
        ' WHERE n.owner_id = ?'
        ' ORDER BY created DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('notes/index.html', notes=notes)

# create blueprint
@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is requred.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO note (title, body, owner_id)'
                ' VALUES (?,?,?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('note.index'))
    return render_template('notes/create.html')

# update blueprint
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    note = get_note(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is requred.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE note SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('note.index'))
    return render_template('notes/update.html', note=note)

# delete blueprint
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_note(id)
    db = get_db()
    db.execute('DELETE FROM note WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('note.index'))