from flask import flash, request, redirect, url_for, Blueprint
from flask_login import login_required, login_user, logout_user

from server import login_manager, bcrypt
from server.views import render
from server.mod_auth.forms import LoginForm, RegisterForm
from server.mod_auth.libs import User, Role

from mongoengine.errors import NotUniqueError

# setup Blueprint
mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/login', methods=['POST', 'GET'])
def login():
	message = ''
	form = LoginForm(request.form)
	user = User(email=form.email.data).get()
	if request.method == 'POST' and user.exists():
		if form.validate() \
			and bcrypt.check_password_hash(user.password, form.password.data) \
			and user.is_active():

			if login_user(user):
				flash('Logged in successfully.')
				return redirect(
					request.args.get('next') 
					or url_for('nest.home'))
		message = 'Login failed.'
	return render('login.html', mod='auth', **locals())


@mod_auth.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))


@mod_auth.route("/register", methods=['POST', 'GET'])
def register():
	message = ''
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate():

			user = User()
			user.name = form.name.data
			user.email = form.email.data
			user.password = bcrypt.generate_password_hash(form.password.data)
			user.role = Role(name='follower').get()

			try:
				user.save()
				if login_user(user):
					flash('Registered and logged in successfully.')
					return redirect(url_for('nest.home'))
				else:
					flash('Login failed.')
					return redirect(url_for('auth.login'))
			except NotUniqueError:
				message = 'Email address already registered. [login?](/login)'
		else:
			message = 'Invalid information.'
	return render('register.html', mod='auth', **locals())


@login_manager.user_loader
def load_user(userid):
	user = User(id=userid).get()
	if user.is_active():
		return user
	else:
		return None


@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('auth.login'))