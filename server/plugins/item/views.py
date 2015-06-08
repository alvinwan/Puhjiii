from flask import request, redirect, url_for
from flask_login import current_user, login_required

from server import mod_nest, mod_public
from server.views import render, context_preset, render_error
from server.nest.libs import Nest
from .libs import Item
from server.plugins.mold.libs import Mold
from server.plugins.preview.interactive import postprocess
from .forms import EditItemForm, AddItemForm

from jinja2.exceptions import TemplateNotFound, TemplatesNotFound
from mongoengine.errors import DoesNotExist


@mod_nest.route("/item/<string:item_mold>/<string:item_id>")
@mod_nest.route("/mold/<string:item_mold>")
@login_required
def mold(item_mold, item_id=None):
	mold = Mold(name=item_mold).get()
	nst = Nest(current_user, request)
	if item_id:
		item = Item(id=item_id).get()
		form = EditItemForm.propagate(mold.info, data=item.info)(request.form)
		nst.load_plugin('item.edit', item=item)
		path = url_for('public.item', item_mold=item_mold, item_id=item_id)
	else:
		nst.load_plugin('item.s', item_mold=item_mold, mold=mold)
		path = '/' + item_mold
	nst.load_plugin('preview.basic', path=path, request=request)
	locals().update(context_preset(nst))
	return render('nest.html', **locals())


def item_form(item_mold, action='add', item_id=None):
	message=''
	mold = Mold(name=item_mold).get()
	class_ = {'add': AddItemForm, 'edit': EditItemForm}[action].propagate(mold.info)
	if item_id:
		item = Item(id=item_id).get()
		form = class_(request.form, data=item.info)
	else:
		form = class_(request.form)
	nst = Nest(current_user, request)
	nst.load_plugin('item.%s' % action)
	if item_id:
		url = url_for('public.item', item_mold=item_mold, item_id=item_id)
		nst.load_plugin('preview.interactive', path=url, request=request, template='public/%s.html' % item_mold,
		                action=url_for('nest.item_iedit', item_mold=item_mold, item_id=item_id), item_id=item_id)
	else:
		nst.load_plugin('preview.basic', path='', request=request)
	locals().update(context_preset(nst))
	if request.method == 'POST' and form.validate():
		if not item_id:
			item = Item()
		item.load(
			info={k: v.data for k, v in form._fields.items()},
			mold=mold).save()
		return redirect(url_for('nest.mold', item_mold=item_mold, item_id=str(item.id)))
	return render('nest.html', **locals())


@mod_nest.route("/item/<string:item_mold>/<string:item_id>/edit", methods=['POST', 'GET'])
@login_required
def item_edit(item_mold, item_id):
	try:
		return item_form(item_mold, 'edit', item_id)
	except DoesNotExist:
		return render('error.html', message='No such %s exists.' % item_mold)


@mod_nest.route("/item/<string:item_mold>/add", methods=['GET', 'POST'])
@login_required
def item_add(item_mold):
	return item_form(item_mold, 'add')


@mod_nest.route("/item/<string:item_mold>/<string:item_id>/iedit", methods=['POST'])
@login_required
def item_iedit(item_mold, item_id):
	try:
		url = url_for('public.item', item_mold=item_mold, item_id=item_id)
		postprocess(url=url, html=request.form['html'])
		return redirect(url_for('nest.item_edit', url=url))
	except DoesNotExist:
		return render('error.html', message='No such %s exists.' % item_mold)


@mod_nest.route("/item/<string:item_mold>/<string:item_id>/delete")
@login_required
def item_delete(item_mold, item_id):
	try:
		Item(id=item_id, mold=Mold(name=item_mold).get()).delete()
		return redirect(url_for('nest.mold', item_mold=item_mold))
	except DoesNotExist:
		return render('error.html', message='No such %s exists.' % item_mold)


@mod_public.route("/<string:variable>")
def items(variable):
	try:
		req = request.args
		if req.get('id', None):
			return item(variable, None)
		path, itms = Item.items(variable, page=req.get('page', 1), per_page=req.get('per_page', 10))
		return render(path, mod='public', **itms)
	except (TemplatesNotFound, TemplateNotFound):
		return render_error('Template not found for page mold.')


@mod_public.route("/<string:item_mold>/<string:item_slug>")
@mod_public.route("/<string:item_mold>/<string:item_id>/")
def item(item_mold, item_slug=None, item_id=None):
	path, itms = Item.item(
		item_mold,
		item_id=item_id,
		item_slug=item_slug)
	return render(path, mod='public', **itms)