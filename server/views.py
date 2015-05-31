import flask
from flask_login import current_user, login_user, login_required, logout_user

from server import app
from server import login_manager

from server.nest import Nest, File, Allow
from server.models import User, Item, LoginForm, RegisterForm, Role


def render(name, check=True, **context):
	if check:
		name = File.name(name)
	return flask.render_template(name, **context)


@app.route("/")
def index():
	return render('index.html')

"""
Login & Register
Handle all user session functionality.
"""


@login_manager.user_loader
def load_user(userid):
	print('LOADING')
	print(userid)
	try:
		return User.objects.fields(id=userid).get()
	except:
		return None


@login_manager.unauthorized_handler
def unauthorized():
	# do stuff
	return ''


@app.route('/login', methods=['POST', 'GET'])
def login():
	form = LoginForm(flask.request.form)
	message = ''
	if flask.request.method == 'POST':
		if form.validate():

			user = User()
			user.email = form.email.data
			user.password = form.password.data

			login_user(user)

			flask.flash('Logged in successfully.')

			# next = flask.request.args.get('next')
			# if not flask.next_is_valid(next):
			# 	return flask.abort(400)

			# return flask.redirect(next or flask.url_for('index'))
			return flask.redirect(flask.url_for('nest'))
		message = 'Invalid input.'
	return render('login.html', **locals())


@app.route("/logout")
@login_required
def logout():
	logout_user()
	return flask.redirect("/")


@app.route("/register", methods=['POST', 'GET'])
def register():
	form = RegisterForm(flask.request.form)
	message = ''
	if flask.request.method == 'POST':
		if form.validate():

			user = User()
			user.name = form.name.data
			user.email = form.email.data
			user.password = form.password.data
			user.role = Role.objects(name='follower').get()
			user.save()

			flask.flash('Registered successfully.')

			return flask.redirect(flask.url_for('login'))
	return render('register.html', **locals())

"""
Nest
The admin, handles Puhjee management system
"""


@app.route("/nest")
@login_required
def nest():
	# if not Allow.ed(current_user, 'access_nest'):
	# 	return flask.redirect('/')
	nst = Nest(current_user, flask.request)
	return render('puhjee.nest.html', nest=nst)


@app.route("/nest/template/<path:template>")
@login_required
def nest_template(template):
	if not Allow.ed(current_user, 'access_nest'):
		return flask.redirect('/')
	nst = Nest(current_user, flask.request)
	nst.aside = nst.sidebar(current_user, 'template')
	nst.section = nst.content(current_user, 'template', path=template)
	return render('puhjee.nest.html', nest=nst)


"""
Items
Handles all repeatable items
"""


@app.route("/<string:items_name>")
def items(items_name):
	req = flask.request.args
	if 'page' in req.keys():
		path, items = Item(File).items(items_name, req['page'], req['per_page'])
	else:
		path, items = Item(File).items(items_name)
	return render(path, **items)


@app.route("/<string:item_name>/<int:id>")
def item(item_name, id):
	path, items = Item(File).item(item_name, id)
	return render(path, **items)