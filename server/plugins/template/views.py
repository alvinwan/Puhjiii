from flask_login import login_required, current_user
from flask import make_response, request

from server import mod_nest
from server.nest.libs import Nest
from server.views import render, context_preset
from os.path import join
import config
import json


@mod_nest.route("/templates")
@login_required
def templates():
	return template('public/index.html')


@mod_nest.route("/api/template/")
@mod_nest.route("/api/template/<path:path>")
@login_required
def api_template(path=''):
	abs_path = join(config.BASE_DIR, 'server/templates', path)
	if request.args.get('context', None):
		return render(path, **json.loads(request.args.get('context')))
	return make_response(open(abs_path).read())


@mod_nest.route("/template/")
@mod_nest.route("/template/<path:templt>")
@login_required
def template(templt=''):
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'template.s', path=templt)
	nst.load_plugin(current_user, 'preview', path=templt)
	return render('nest.html', **context_preset(nst))