from flask import request, redirect, url_for
from flask_login import current_user, login_required

from server.views import render, context_preset
from server.nest.libs import Nest
from server import mod_nest, mod_public

from .libs import Page
from .forms import AddPageForm, EditPageForm

import config
from os.path import join, isdir
from os import listdir

from jinja2.exceptions import TemplateNotFound
from mongoengine.errors import NotUniqueError, DoesNotExist

for url in Page.model.objects().all():
	mod_public.add_url_rule(
		join('/', url.url),
		url.title,
		lambda: render(url.template, mod='public', **url.info))


@mod_nest.route("/page/add", methods=['POST', 'GET'])
@login_required
def page_add():
	form = AddPageForm(request.form)
	if request.method == 'POST' and form.validate():
		try:
			render("public/"+form.template.data)
			Page(title=form.title.data,
			    template=form.template.data,
			    url=form.url.data,
			    info=Page.parse(form.template.data)).save()
			return redirect(url_for('nest.page_edit', url=form.url.data))
		except (TemplateNotFound, FileNotFoundError):
			message = 'No such template exists.'
		except NotUniqueError:
			message = 'URL already taken by another page.'
	else:
		dir = join(config.BASE_DIR, 'server/templates/public')
		form.template.choices = [(f, f) for f in listdir(dir) if not isdir(join(dir, f))]
		nst = Nest(current_user, request)
		nst.load_plugin(current_user, 'page.add')
		nst.load_plugin(current_user, 'preview', path='', request=request)
		locals().update(context_preset(nst))
	return render('nest.html', **locals())


@mod_nest.route("/page/edit/<path:url>", methods=['GET', 'POST'])
@login_required
def page_edit(url):
	page = Page(url=url).get()
	form = EditPageForm(request.form, page)
	if request.method == 'POST':
		try:
			page.load(
				url=form.url.data,
				title=form.title.data,
				template=form.template.data,
				info=Page.parse(form.template.data)).save()
			return redirect(url_for('nest.pages'))
		except DoesNotExist:
			return render('error.html', message='No such page exists.')
	else:
		dir = join(config.BASE_DIR, 'server/templates/public')
		form.template.choices = [(f, f) for f in listdir(dir) if not isdir(join(dir, f))]
		nst = Nest(current_user, request)
		nst.load_plugin(current_user, 'page.edit')
		nst.load_plugin(current_user, 'preview', path=url, request=request)
		locals().update(context_preset(nst))
	return render('nest.html', **locals())


@mod_nest.route("/page/delete/<path:url>")
@login_required
def page_delete(url):
	try:
		Page(url=url).delete()
	except DoesNotExist:
		return render('error.html', message='No such page exists.')
	return redirect(url_for('nest.pages'))


@mod_nest.route("/pages")
@mod_nest.route("/page/<path:url>")
@login_required
def pages(url=''):
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'page.s')
	nst.load_plugin(current_user, 'preview', path=url, request=request)
	return render('nest.html', **context_preset(nst))