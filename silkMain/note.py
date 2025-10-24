from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from datetime import datetime

from silkMain.auth import login_required
from silkMain.db import get_db

bp = Blueprint('note', __name__)

# views

# default view
@bp.route('/')
@login_required
def index():
    db = get_db()
    notes = db.execute(
        'SELECT n.id, title, body, created, modified, owner_id'
        ' FROM note n'
        ' WHERE n.owner_id = ?'
        ' ORDER BY modified ASC',
        (g.user['id'],)
    ).fetchall()
    return render_template('notes/index.html', notes=notes)

# create view
@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            title = 'Untitled'

        db = get_db()
        db.execute(
            'INSERT INTO note (title, body, owner_id)'
            ' VALUES (?,?,?)',
            (title, body, g.user['id'])
        )
        db.commit()
        return redirect(url_for('note.index'))
    return render_template('notes/create.html')

# update view
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    note = get_db().execute(
        'SELECT n.id, title, body, created, modified, owner_id'
        ' FROM note n'
        ' WHERE n.id = ?',
        (id,)
    ).fetchone()

    if note is None:
        abort(404, f"Note id {id} doesn't exist.")

    if note['owner_id'] !=g.user['id']:
        abort(403)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        
        if not title:
            title = 'Untitled'

        db = get_db()
        db.execute(
            'UPDATE note SET title = ?, body = ?, modified = ?'
            ' WHERE id = ?',
            (title, body, datetime.now().isoformat(), id)
        )
        db.commit()
        return redirect(url_for('note.index'))
    return render_template('notes/update.html', note=note)

# delete view
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    note = get_db().execute(
        'SELECT n.id, owner_id'
        ' FROM note n'
        ' WHERE n.id = ?',
        (id,)
    ).fetchone()

    if note is None:
        abort(404, f"Note id {id} doesn't exist.")

    if note['owner_id'] !=g.user['id']:
        abort(403)
    db = get_db()
    db.execute('DELETE FROM note WHERE id = ?', (id,))
    db.commit()
    flash('Note successfully deleted')
    return redirect(url_for('note.index'))