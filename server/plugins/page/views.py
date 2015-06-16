from flask import request, redirect, url_for
from flask_login import current_user, login_required
from server.auth.libs import Alert
from server.views import render, context, render_error, redirect_error
from server.nest.libs import Nest
from server import mod_nest, mod_public
from .libs import Page
from .forms import AddPageForm, EditPageForm
from server.plugins.code.libs import Template
from server.plugins.preview.interactive import postprocess
from os.path import join
from jinja2.exceptions import TemplateNotFound
from mongoengine.errors import NotUniqueError, DoesNotExist


@mod_nest.route("/pages")
@mod_nest.route("/page/")
@mod_nest.route("/page/<path:url>")
@login_required
def pages(url=''):
	nest = Nest(current_user, request)
	nest.load_plugin('page.s')
	nest.load_plugin('preview.basic', path=url, request=request)
	return render('nest.html', **context(nest))


def page_form(page, form, plugins, error, alert):
	nest = Nest(current_user, request)
	try:
		nest.load_plugins(*plugins)
		form.populate_templates()
		if request.method == 'POST' and form.validate():
			render("public/"+form.template.data)
			template = Template(path="public/"+form.template.data).get()
			page.load(title=form.title.data,
			     template="public/"+form.template.data,
			     url=form.url.data,
			     info=template.defaults).save()
			alert.log()
			return redirect(url_for('nest.page_edit', id=page.id))
		if form.errors:
			Alert(form.error()).log()
		response = render('nest.html', **context(**locals()))
		response.headers.add('X-XSS-Protection', 0)
		return response
	except (TemplateNotFound, FileNotFoundError) as e:
		message = 'No such template exists: '+str(e)
	except NotUniqueError:
		message = 'URL and/or title already taken by another page.'
	except DoesNotExist as e:
		Template().import_path(path="public/"+form.template.data).save()
		return page_form(page, form, plugins, error, alert)
	return redirect_error(message, error)


@mod_nest.route("/page/add", methods=['POST', 'GET'])
@login_required
def page_add():
	return page_form(
		page=Page(),
		form=AddPageForm(request.form),
	    error=url_for('nest.page_add'),
	    alert=Alert('Page created.', class_='okay'),
		plugins=[
			('page.add', {}),
			('preview.basic',
				{'path': '', 'request': request})])


@mod_nest.route("/page/edit/<string:id>", methods=['GET', 'POST'])
@login_required
def page_edit(id):
	try:
		page = Page(id=id).get()
		page.template = page.template.replace('public/', '')
		return page_form(
			page=page,
			form=EditPageForm(request.form, page),
		    error=url_for('nest.page_edit', id=id),
		    alert=Alert('Page %s updated.' % page.url, class_='okay'),
		    plugins=[
			    ('page.edit', {}),
			    ('preview.interactive',
			        {
			            'path': page.url,
			            'request': request,
			            'action': url_for('nest.page_iedit', id=id)
			        }
			    )
		    ])
	except DoesNotExist as e:
		return redirect_error(str(e), url_for('nest.pages'))


@mod_nest.route("/page/iedit/<string:id>", methods=['POST'])
@login_required
def page_iedit(id):
	try:
		page = Page(id=id).get()
		template = Template(path=page.template).get()
		postprocess(
			html=request.form['html'], 
			template=template, 
			host=page,
			partials=request.form['partials'],
			molds=request.form['molds'])
		return redirect(url_for('nest.page_edit', id=id))
	except DoesNotExist as e:
		return redirect_error(str(e), url_for('nest.pages'))


@mod_nest.route("/page/delete/<string:id>")
@login_required
def page_delete(id):
	try:
		Page(id=id).delete()
		Alert('Paged %s deleted' % page.url, class_='okay').log()
		return redirect(url_for('nest.pages'))
	except DoesNotExist:
		return redirect_error('No such page exists.', url_for('nest.pages'))


for page in Page.model.objects().all():
	def generate(page):
		def helper():
			nonlocal page
			try:
				page.reload()
			except DoesNotExist:
				page = Page.model.objects(url=page.url).get()
			return render(page.template, mod='public', **page.info)
		mod_public.add_url_rule(join('/', page.url), page.title, helper)
	generate(page)