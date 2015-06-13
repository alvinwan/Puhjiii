from flask_login import login_required, current_user
from flask import make_response, request, redirect, url_for

from server import mod_nest
from server.nest.libs import Nest
from server.views import render, context, redirect_error
from .forms import EditCodeForm, ImportCodeForm, UploadCodeForm
from .libs import Template
from server.auth.libs import File, Alert
import json

from mongoengine.errors import DoesNotExist, NotUniqueError


@mod_nest.route("/code")
@login_required
def codes():
	return code()


@mod_nest.route("/api/code/")
@mod_nest.route("/api/code/<path:path>")
@login_required
def api_code(path=''):
	if request.args.get('context', None):
		return render(path, **json.loads(request.args.get('context')))
	return make_response(File.read(path))


@mod_nest.route("/code/")
@mod_nest.route("/code/<path:path>", methods=['GET', 'POST'])
@login_required
def code(path='templates/public/index.html'):
	nest = Nest(current_user, request)
	try:
		nest.load_plugin('code.s', path=path)
		form = EditCodeForm(request.form, path=path)
		if request.method == 'POST':
			File.write(path, form.code.data)
		nest.load_plugin('code.edit', path=path)
		form.code.data = File.read(path)+'\n'
	except IsADirectoryError:
		pass
	except UnicodeDecodeError:
		pass
	return render('nest.html', **context(**locals()))


@mod_nest.route("/code/import", methods=['POST', 'GET'])
@login_required
def code_import():
	form = ImportCodeForm(request.form)
	nest = Nest(current_user, request)
	try:
		if request.method == 'POST':
			template = Template(path=form.path.data).load(html=form.html.data).import_html().save()
			Alert('File "%s" imported.' % form.path.data, class_='okay').log()
			return redirect(url_for('nest.code', path='templates/'+form.path.data))
		nest.load_plugin('code.import')
		return render('nest.html', **context(**locals()))
	except NotUniqueError as e:
		return redirect_error(str(e))


@mod_nest.route("/code/upload", methods=['POST', 'GET'])
@login_required
def code_upload():
	form = UploadCodeForm(request.form)
	nest = Nest(current_user, request)
	try:
		if request.method == 'POST':
			message = ''
			for file in request.files.values():
				filename = file.filename.replace('../', '')
				Template(path='public/%s' % filename).load(html=file.read()).import_html().save()
				Alert('File "%s" uploaded.' % filename, class_='okay').log()
				redirect(url_for('nest.codes'))
		nest.load_plugin('code.upload')
		return render('nest.html', **context(**locals()))
	except NotUniqueError as e:
		return redirect_error(str(e))
		