from flask import request, redirect, url_for
from flask_login import current_user, login_required

from server.views import render, context_preset
from server.nest.libs import Nest
from server import mod_nest, mod_public

from .libs import Page
from .forms import AddPageForm, EditPageForm
from server.plugins.code.libs import Template
from server.plugins.preview.interactive import postprocess

import config
from os.path import join, isdir
from os import listdir

from jinja2.exceptions import TemplateNotFound
from mongoengine.errors import NotUniqueError, DoesNotExist

for page in Page.model.objects().all():
	def temp():
		page.reload()
		return render('public/%s' % page.template, mod='public', **page.info)
	mod_public.add_url_rule(
		join('/', page.url),
		page.title,
		temp)


@mod_nest.route("/page/add", methods=['POST', 'GET'])
@login_required
def page_add():
	form = AddPageForm(request.form)
	dir = join(config.BASE_DIR, 'server/templates/public')
	form.template.choices = [(f, f) for f in listdir(dir) if not isdir(join(dir, f))]
	if request.method == 'POST' and form.validate():
		try:
			render("public/"+form.template.data)
			template = Template(path="public/"+form.template.data).get()
			Page(title=form.title.data,
			    template=form.template.data,
			    url=form.url.data,
			    info=template.defaults).save()
			return redirect(url_for('nest.page_edit', url=form.url.data))
		except (TemplateNotFound, FileNotFoundError):
			message = 'No such template exists.'
		except NotUniqueError:
			message = 'URL already taken by another page.'
	else:
		nst = Nest(current_user, request)
		nst.load_plugin('page.add')
		nst.load_plugin('preview.basic', path='', request=request)
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
				template=form.template.data).save()
			return redirect(url_for('nest.pages'))
		except DoesNotExist:
			return render('error.html', message='No such page exists.')
	else:
		dir = join(config.BASE_DIR, 'server/templates/public')
		form.template.choices = [(f, f) for f in listdir(dir) if not isdir(join(dir, f))]
		nst = Nest(current_user, request)
		nst.load_plugin('page.edit')
		nst.load_plugin('preview.interactive', path=url, request=request, 
		                action=url_for('nest.page_iedit', url=url))
		locals().update(context_preset(nst))
	return render('nest.html', **locals())


@mod_nest.route("/page/iedit/<path:url>", methods=['POST'])
@login_required
def page_iedit(url):
	postprocess(url=url, html=request.form['html'])
	return redirect(url_for('nest.page_edit', url=url))


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
	nst.load_plugin('page.s')
	nst.load_plugin('preview.basic', path=url, request=request)
	return render('nest.html', **context_preset(nst))