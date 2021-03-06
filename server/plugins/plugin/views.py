from server import mod_nest
from server.nest.libs import Nest
from .libs import Plugin
from server.views import context, render, redirect_error, permission_required
from flask_login import login_required, current_user
from flask import request, url_for, redirect

from mongoengine.errors import DoesNotExist

@mod_nest.route("/plugins")
@permission_required('access_plugins')
@login_required
def plugins():
	nest = Nest(current_user, request).load_plugin('plugin.s')
	return render('nest.html', **context(nest))


def plugin_update(plugin_name, **kwargs):
	try:
		Plugin(name=plugin_name).load(**kwargs).save()
		return redirect(url_for('nest.plugins'))
	except DoesNotExist:
		return redirect_error('No such plugin "%s" found.' % plugin_name, url_for('nest.plugins'))


@mod_nest.route("/plugin/<string:plugin_name>/deactivate")
@permission_required('access_plugins')
@login_required
def plugin_deactivate(plugin_name):
	if plugin_name in ['code', 'item', 'mold', 'page', 'plugin', 'preview', 'navbar', 'setting']:
		return redirect_error('Plugin "%s" is essential to Puhjiii\'s function; it cannot be deactivated.' % plugin_name,
		                      url_for('nest.plugins'))
	return plugin_update(plugin_name, is_active=False)


@mod_nest.route("/plugin/<string:plugin_name>/activate")
@permission_required('access_plugins')
@login_required
def plugin_activate(plugin_name):
	return plugin_update(plugin_name, is_active=True)