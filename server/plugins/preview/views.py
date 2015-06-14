from flask import render_template
from server import mod_nest
from server.plugins.page.libs import Page
from flask_login import login_required


@mod_nest.route("/iedit/")
@mod_nest.route("/iedit/<path:path>")
@login_required
def iedit(path='/'):
	page = Page(url=path).get()
	return render_template('plugins/preview/wrapper.html', template=page.template, **page.info)