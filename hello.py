#! /bin/env/python
import os
from datetime import datetime
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)

db = SQLAlchemy(app)
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)

	def __repr__(self):
		return '<Role %r>' % self.name
	users = db.relationship('User', backref='role')

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)

	def __repr__(self):
		return '<User %r>' % self.username
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')

bootstrap = Bootstrap(app)
moment = Moment(app)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
@app.route('/', methods=['GET', 'POST'])
def index():
	# name = None
	# form = NameForm()
	# if form.validate_on_submit():
	# 	old_name = session.get('name')
	# 	if old_name is not None and old_name != form.name.data:
	# 		flash('Looks like you have changed your name!')
	# 	session['name'] = form.name.data
	# 	# form.name.data = ''
	# 	return redirect(url_for('index'))
	# return render_template('index.html', form=form, name=session.get('name'))
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form = form, name = session.get('name'),
		known = session.get('known', False))

@app.route('/user/<name>')
def user(name):
	return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500
if __name__=='__main__':
	manager.run()
