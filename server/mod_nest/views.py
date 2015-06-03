import config
from flask import request, Blueprint, redirect, make_response
from flask_login import current_user, login_required

from server.views import render
from server.mod_nest.libs import Nest
from server.mod_auth.libs import Allow

# setup Blueprint
mod_nest = Blueprint('nest', __name__, url_prefix='/nest')


def permission_required(permission=None, dest='/'):
	def decorator(f):
		def helper():
			if not Allow.ed(current_user, permission):
				return redirect(dest)
			return f()
		return helper
	return decorator


def mod_preset(nest):
	context = {
		'repeats': 1,
		'markdown': False,
		'nest': nest,
	    'mod': 'nest'
	}
	context.update(nest.context)
	return context


@mod_nest.route("/")
@login_required
# @permission_required('access_nest', '/login')
def home():
	return preview()


@mod_nest.route("/templates")
@login_required
def templates():
	return template('public/index.html')


@mod_nest.route("/api/template/")
@mod_nest.route("/api/template/<path:path>")
@login_required
def api_template(path=''):
	return make_response(open(config.BASE_DIR+'/server/templates/'+path).read())
	

@mod_nest.route("/template/")
@mod_nest.route("/template/<path:templt>")
@login_required
def template(templt=''):
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'navfiles', path=templt)
	nst.generate_section(current_user, 'preview', path=templt)
	return render('nest.html', **mod_preset(nst))


@mod_nest.route("/items")
@login_required
def items():
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'navbar')
	nst.generate_section(current_user, 'preview', path='', request=request)
	return render('nest.html', **mod_preset(nst))


@mod_nest.route("/preview")
@mod_nest.route("/preview/<path:url>")
@login_required
def preview(url=''):
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'navbar')
	nst.generate_section(current_user, 'preview', path=url, request=request)
	return render('nest.html', **mod_preset(nst))