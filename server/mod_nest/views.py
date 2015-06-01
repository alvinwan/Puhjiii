from flask import request, Blueprint, redirect
from flask_login import current_user, login_required

from server.views import render
from server.mod_nest.libs import Nest
from server.mod_auth.libs import Allow

# setup Blueprint
mod_nest = Blueprint('nest', __name__, url_prefix='/nest')

@mod_nest.route("/")
@login_required
def home():
	if not Allow.ed(current_user, 'access_nest'):
		return redirect('/')
	nst = Nest(current_user, request)
	return render('nest.html', mod='nest', nest=nst)


@mod_nest.route("/template/<path:template>")
@login_required
def template(template):
	if not Allow.ed(current_user, 'access_nest'):
		return redirect('/')
	nst = Nest(current_user, request)
	nst.aside = nst.sidebar(current_user, 'template')
	nst.section = nst.content(current_user, 'template', path=template)
	return render('nest.html', mod='nest', nest=nst)