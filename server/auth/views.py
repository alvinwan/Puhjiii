from flask import request, redirect, url_for, Blueprint
from flask_login import login_required, login_user, logout_user
from server import login_manager, bcrypt
from server.views import render
from .forms import LoginForm, RegisterForm
from .libs import User, Role
from mongoengine.errors import NotUniqueError, ValidationError, DoesNotExist

# setup Blueprint
mod_auth = Blueprint('auth', __name__)


@mod_auth.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm(request.form)
	user = User(email=form.email.data)
	try:
		if request.method == 'POST' and form.validate():
			user.get()
			if user.exists() and user.is_active() \
				and bcrypt.check_password_hash(user.password, form.password.data):

				if login_user(user):
					return redirect(request.args.get('next') or url_for('nest.home'))
			message = 'Login failed.'
	except ValidationError as e:
		message = str(e)
	except DoesNotExist:
		message = 'Login failed.'
	return render('login.html', mod='auth', **locals())


@mod_auth.route("/register", methods=['POST', 'GET'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST':
		try:
			form.validate()
			if User.model.objects().all().count() == 0:
				role_name = 'owner'
			else:
				role_name = 'follower'

			user = User(
				name=form.name.data,
				email=form.email.data,
				password=bcrypt.generate_password_hash(form.password.data),
				role=Role(name=role_name).get()
			).save()
			if login_user(user):
				return redirect(url_for('nest.home'))
			else:
				return redirect(url_for('auth.login'))
		except (DoesNotExist, ValidationError) as e:
			message = str(e)
		except NotUniqueError:
			message = 'Email address already registered. [login?](/login)'
	return render('register.html', mod='auth', markdown=True, **locals())


@mod_auth.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))


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