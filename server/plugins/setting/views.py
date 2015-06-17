from server import mod_nest
from flask import request
from flask_login import login_required, current_user
from server.nest.libs import Nest
from server.views import render, context, permission_required


@mod_nest.route("/settings")
@login_required
@permission_required('access_settings')
def settings():
	nest = Nest(current_user, request)
	nest.load_plugin('setting.s')
	return render("nest.html", **context(nest))