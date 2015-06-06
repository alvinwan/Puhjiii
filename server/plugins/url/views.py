from flask import request, redirect
from flask_login import current_user, login_required

from server.views import render, context_preset
from server.mod_nest.views import mod_nest
from server.mod_nest.libs import Nest
from server.mod_public.libs import URL
from server.mod_public.forms import AddURLForm, EditURLForm

from jinja2.exceptions import TemplateNotFound

@mod_nest.route("/url/add", methods=['POST', 'GET'])
@login_required
def url_add():
	message=''
	form = AddURLForm(request.form)
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'url.add')
	nst.load_plugin(current_user, 'preview', path='', request=request)
	locals().update(context_preset(nst))
	if request.method == 'POST' and form.validate():
		try:
			render("public/"+form.template.data)
			URL(title=form.title.data,
			    template=form.template.data,
			    url=form.url.data,
			    info=URL.parse(form.template.data)).save()
			return redirect("/nest/url/edit/%s" % form.url.data)
		except (TemplateNotFound, FileNotFoundError):
			message = 'No such template exists.'
	return render('nest.html', **locals())


@mod_nest.route("/url/edit/<path:url>")
@login_required
def url_edit(url):
	page = URL(url=url).get()
	form = EditURLForm(request.form).propagate(page.info)(request.form)
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'url.edit')
	nst.load_plugin(current_user, 'preview', path=url, request=request)
	return render('nest.html', **context_preset(nst))


@mod_nest.route("/urls")
@mod_nest.route("/url/<path:url>")
@login_required
def urls(url=''):
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'url.s')
	nst.load_plugin(current_user, 'preview', path=url, request=request)
	return render('nest.html', **context_preset(nst))