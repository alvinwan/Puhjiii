from server import mod_nest
from server.nest.libs import Nest
from .libs import Plugin
from server.views import context_preset, render
from flask_login import login_required, current_user
from flask import request, url_for, redirect

from mongoengine.errors import DoesNotExist

@mod_nest.route("/plugins")
@login_required
def plugins():
	nst = Nest(current_user, request)
	nst.load_plugin('plugin.s')
	locals().update(**context_preset(nst))
	return render('nest.html', **locals())


@mod_nest.route("/plugin/<string:plugin_name>/deactivate")
@login_required
def plugin_deactivate(plugin_name):
	try:
		Plugin(name=plugin_name).load(is_active=False).save()
		return redirect(url_for('plugins'))
	except DoesNotExist:
		return render('error.html', message='No such plugin "%s" found.' % plugin_name)


@mod_nest.route("/plugin/<string:plugin_name>/activate")
@login_required
def plugin_activate(plugin_name):
	try:
		Plugin(name=plugin_name).load(is_active=True).save()
		return redirect(url_for('plugins'))
	except DoesNotExist:
		return render('error.html', message='No such plugin "%s" found.' % plugin_name)
