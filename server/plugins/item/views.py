from flask import request, redirect
from flask_login import current_user, login_required

from server import mod_nest, mod_public
from server.views import render, context_preset, render_error
from server.nest.libs import Nest
from .libs import Item
from server.plugins.type.libs import Type
from .forms import EditItemForm, AddItemForm

from jinja2.exceptions import TemplateNotFound, TemplatesNotFound

@mod_nest.route("/items")
@login_required
def types():
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'type.s')
	nst.load_plugin(current_user, 'preview', path='', request=request)
	return render('nest.html', **context_preset(nst))


@mod_nest.route("/item/<string:item_type>/<string:item_id>")
@mod_nest.route("/item/<string:item_type>")
@login_required
def items(item_type, item_id=None):
	type = Type(name=item_type).get()
	nst = Nest(current_user, request)
	if item_id:
		item = Item(id=item_id).get()
		form = EditItemForm.propagate(type.info, data=item.info)(request.form)
		nst.load_plugin(current_user, 'item.edit', item=item)
		path = '/%s?id=%s' % (item_type, item_id)
	else:
		nst.load_plugin(current_user, 'item.s', item_type=item_type, type=type)
		path = '/' + item_type
	nst.load_plugin(current_user, 'preview', path=path, request=request)
	locals().update(context_preset(nst))
	return render('nest.html', **locals())


def item_form(item_type, action='add', item_id=None):
	message=''
	type = Type(name=item_type).get()
	class_ = {'add': AddItemForm, 'edit': EditItemForm}[action]
	form = class_.propagate(type.info)(request.form)
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'item.add')
	nst.load_plugin(current_user, 'preview', path='', request=request)
	locals().update(context_preset(nst))
	if request.method == 'POST' and form.validate():
		Item(
			info={k: v.data for k, v in form._fields.items()},
			type=type,
			id=item_id).save()
		return redirect("/nest/item/"+item_type)
	return render('nest.html', **locals())


@mod_nest.route("/item/<string:item_type>/<string:item_id>/edit", methods=['POST'])
@login_required
def item_edit(item_type, item_id):
	return item_form(item_type, 'edit', item_id)


@mod_nest.route("/item/<string:item_type>/add", methods=['GET', 'POST'])
@login_required
def item_add(item_type):
	return item_form(item_type, 'add')


@mod_public.route("/<string:variable>")
def items(variable):
	try:
		req = request.args
		if req.get('id', None):
			return item(variable, None)
		path, itms = Item.items(variable, page=req.get('page', 1), per_page=req.get('per_page', 10))
		return render(path, mod='public', **itms)
	except (TemplatesNotFound, TemplateNotFound):
		return render_error('Template not found for page type.')


@mod_public.route("/<string:item_name>/<string:item_slug>")
def item(item_name, item_slug):
	path, itms = Item.item(
		item_name,
		item_id=request.args.get('id', None),
		item_slug=item_slug)
	return render(path, mod='public', **itms)