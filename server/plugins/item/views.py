from flask import request, redirect
from flask_login import current_user, login_required

from server.views import render, context_preset
from server.mod_nest.views import mod_nest
from server.mod_nest.libs import Nest
from server.mod_public.libs import Type, Item
from server.mod_public.forms import EditItemForm, AddItemForm

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