from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/main/index', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        return redirect(url_for('/main/index'))
    return render_template('main/index.html', form=form, name=session.get('name'),
                        known=session.get('known', False),
                        current_time=datetime.utcnow())

@main.route('/main/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('main/user.html', user=user)