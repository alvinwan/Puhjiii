from flask import request, redirect, url_for
from flask_login import current_user, login_required

from server import mod_nest, mod_public
from server.plugins.page.libs import Page
from server.views import render, context, render_error
from server.nest.libs import Nest
from .libs import Item
from server.plugins.mold.libs import Mold
from .forms import EditItemForm, AddItemForm

from jinja2.exceptions import TemplateNotFound, TemplatesNotFound
from mongoengine.errors import DoesNotExist


"""

Nest URLs

"""


def nest_items(item_mold, url):
	nest = Nest(current_user, request)
	try:
		mold = Mold(name=item_mold).get()
		nest.load_plugin('item.s', item_mold=item_mold, mold=mold)
		nest.load_plugin('preview.basic',
		                 path=url,
		                 request=request)
		return render('nest.html', **context(**locals()))
	except DoesNotExist as e:
		return render_error(str(e))


@mod_nest.route("/mold/<string:item_mold>")
@login_required
def mold(item_mold):
	return nest_items(
		item_mold=item_mold, 
		url=url_for('public.items', item_mold=item_mold))


@mod_nest.route("/item/<string:item_mold>/<string:item_id>")
@login_required
def item(item_mold, item_id):
	return nest_items(
		item_mold=item_mold,
		url=url_for('public.item', item_mold=item_mold, item_id=item_id))


def item_form(mold, item, form, plugins, forward, item_mold, item_id=None):
	nest = Nest(current_user, request)
	try:
		nest.load_plugins(*plugins)
		if request.method == 'POST' and form.validate():
			item.load(mold=mold).assemble(form).save()
			return redirect(forward)
		return render('nest.html', **context(**locals()))
	except RuntimeError as e:
		return render_error(str(e))


@mod_nest.route("/item/<string:item_mold>/<string:item_id>/edit", methods=['POST', 'GET'])
@login_required
def item_edit(item_mold, item_id):
	try:
		mold = Mold(name=item_mold).get()
		item = Item(id=item_id).get()
		return item_form(
			mold=mold,
		    item=item,
		    form=EditItemForm.propagate(mold.info)(request.form, **item.info),
		    plugins = [
			    ('item.edit', {}),
			    ('preview.basic',
			        {
			            'request': request,
			            'path': url_for('public.item', item_mold=item_mold, item_id=item_id)
			        }
			    )
		    ],
		    forward=url_for('nest.mold', item_mold=item_mold),
		    item_mold=item_mold,
		    item_id=item_id
		)
	except DoesNotExist as e:
		return render_error(str(e))


@mod_nest.route("/item/<string:item_mold>/add", methods=['GET', 'POST'])
@login_required
def item_add(item_mold):
	try:
		mold = Mold(name=item_mold).get()
		return item_form(
			mold=mold,
			item=item,
		    form=AddItemForm.propagate(mold.info)(request.form),
			plugins = [
				('item.add', {}),
				('preview.basic',
					{
						'request': request,
						'path': url_for('public.items', item_mold=item_mold)
					}
				)
			],
		    forward=url_for('nest.mold', item_mold=item_mold),
			item_mold=item_mold
		)
	except DoesNotExist as e:
		return render_error(str(e))


@mod_nest.route("/item/<string:item_mold>/<string:item_id>/delete")
@login_required
def item_delete(item_mold, item_id):
	try:
		Item(id=item_id, mold=Mold(name=item_mold).get()).delete()
		return redirect(url_for('nest.mold', item_mold=item_mold))
	except DoesNotExist as e:
		return render_error(str(e))


"""

Public URLs

"""

@mod_public.route("/<string:item_mold>")
def items(item_mold):
	try:
		page = Page(url=item_mold).get()
		return render(page.template, mod='public', **page.info)
	except DoesNotExist:
		try:
			req = request.args
			if req.get('id', None):
				return item(item_mold, None)
			path, itms = Item.items(item_mold, page=req.get('page', 1), per_page=req.get('per_page', 10))
			return render(path, mod='public', **itms)
		except (TemplatesNotFound, TemplateNotFound):
			return render_error('Template not found for page mold.')


@mod_public.route("/<string:item_mold>/<string:item_slug>")
@mod_public.route("/<string:item_mold>/<string:item_id>/")
def item(item_mold, item_slug=None, item_id=None):
	try:
		path, itms = Item.item(
			item_mold,
			item_id=item_id,
			item_slug=item_slug)
		return render(path, mod='public', **itms)
	except (TemplatesNotFound, TemplateNotFound):
		return render_error('Template not found for page mold.')