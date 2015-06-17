from shutil import Error
from flask_login import login_required, current_user
from flask import make_response, request, redirect, url_for

from server import mod_nest
from server.nest.libs import Nest
from server.views import render, context, redirect_error, permission_required
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
@permission_required('access_codes')
@login_required
def api_code(path=''):
	if request.args.get('context', None):
		return render(path, **json.loads(request.args.get('context')))
	return make_response(File.read(path))


@mod_nest.route("/code/")
@mod_nest.route("/code/<path:path>", methods=['GET', 'POST'])
@permission_required('access_codes')
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
	except FileNotFoundError:
		return redirect_error('No such path "%s" found.' % path, url_for('nest.code'))
	return render('nest.html', **context(**locals()))


@mod_nest.route("/code/import", methods=['POST', 'GET'])
@permission_required('access_codes')
@login_required
def code_import():
	form = ImportCodeForm(request.form)
	nest = Nest(current_user, request)
	try:
		if request.method == 'POST' and form.validate():
			template = Template(path=form.path.data).import_html(form.html.data).save()
			Alert('File "%s" imported. [View code](%s).' % form.path.data, class_='okay').log()
			return redirect(url_for('nest.code', path='templates/'+form.path.data))
		nest.load_plugin('code.import')
		return render('nest.html', **context(**locals()))
	except NotUniqueError as e:
		return redirect_error(str(e))


@mod_nest.route("/code/upload", methods=['POST', 'GET'])
@permission_required('access_codes')
@login_required
def code_upload():
	form = UploadCodeForm(request.form)
	nest = Nest(current_user, request)
	try:
		if request.method == 'POST' and form.validate():
			for file in request.files.values():
				Template().upload(file, form.destination.data, form.override.data)
				Alert('File "%s" uploaded.' % file.filename, class_='okay').log()
				return redirect(url_for('nest.codes'))
		nest.load_plugin('code.upload')
		return render('nest.html', **context(**locals()))
	except (NotUniqueError, Error) as e:
		message = str(e)
	except IsADirectoryError:
		message = 'Cannot upload directories, sorry. :('
	except FileNotFoundError as e:
		return redirect_error(str(e), url_for('nest.code'))
	return redirect_error(message)