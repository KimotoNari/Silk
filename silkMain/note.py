from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from silkMain.auth import login_required
from silkMain.db import get_db

bp = Blueprint('note', __name__)

# views

@bp.route('/')
def index():
    db = get_db()
    notes = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('note/index.html', notes=notes)