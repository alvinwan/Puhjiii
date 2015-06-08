from flask_login import login_required, current_user
from flask import make_response, request, redirect, url_for

from server import mod_nest
from server.nest.libs import Nest
from server.views import render, context_preset
from .forms import EditCodeForm, ImportCodeForm
from .libs import Template
from os.path import join
import config
import json


@mod_nest.route("/code")
@login_required
def codes():
	return code()


@mod_nest.route("/api/code/")
@mod_nest.route("/api/code/<path:path>")
@login_required
def api_code(path=''):
	abs_path = join(config.BASE_DIR, 'server', path)
	if request.args.get('context', None):
		return render(path, **json.loads(request.args.get('context')))
	return make_response(open(abs_path).read())


@mod_nest.route("/code/")
@mod_nest.route("/code/<path:path>", methods=['GET', 'POST'])
@login_required
def code(path='templates/public/index.html'):
	nst = Nest(current_user, request)
	nst.load_plugin('code.s', path=path)
	try:
		form = EditCodeForm(request.form, path=path)
		if request.method == 'POST':
			Template.html_to_path(form.code.data, path)
		form.code.data = Template.path_to_html(path)
		nst.load_plugin('code.edit', path=path)
	except IsADirectoryError:
		pass
	locals().update(context_preset(nst))
	return render('nest.html', **locals())


@mod_nest.route("/code/import", methods=['POST', 'GET'])
@login_required
def code_import():
	form = ImportCodeForm(request.form)
	if request.method == 'POST':
		template = Template(path=form.path.data).load(
			html=form.html.data
		).import_html().save()
		return redirect(url_for('nest.codes'))
	else:
		nst = Nest(current_user, request)
		nst.load_plugin('code.import')
		locals().update(context_preset(nst))
	return render('nest.html', **locals())