from flask import request, Blueprint, make_response
from flask_login import current_user, login_required

from server.views import render, context_preset
from server.nest.libs import Nest

# setup Blueprint
mod_nest = Blueprint('nest', __name__, url_prefix='/nest')


@mod_nest.route("/")
@login_required
def home():
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'navbar')
	nst.load_plugin(current_user, 'preview', path='', request=request)
	return render('nest.html', **context_preset(nst))


@mod_nest.route("/settings")
@login_required
def settings():
	return make_response('<a href="/nest">main</a>No settings')