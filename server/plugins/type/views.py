from flask import request, redirect, url_for
from flask_login import current_user, login_required

from server.views import render, context_preset
from server.mod_nest.views import mod_nest
from server.mod_nest.libs import Nest
from server.mod_public.libs import Type
from server.mod_public.forms import AddTypeForm, EditTypeForm

from mongoengine.errors import NotUniqueError


def type_form(action, item_type=None):
	message=''
	type = Type(name=item_type).get()
	form = {'add': AddTypeForm, 'edit': EditTypeForm}[action](
		request.form, data=type.str_fields().data())
	nst = Nest(current_user, request)
	nst.load_plugin(current_user, 'type.%s' % action)
	nst.load_plugin(current_user, 'preview', path='', request=request)
	locals().update(context_preset(nst))
	if request.method == 'POST' and form.validate():
		try:
			type.load(name=form.name.data).add_fields(form.info.data).save()
			if action == 'add':
				return redirect(url_for('nest.types'))
			else:
				return redirect('/nest/item/'+item_type)
		except NotUniqueError:
			message = 'A group of items with that name already exists.'
		except ValueError:
			message = 'Second field should contain fields like "first, last, middle" and may contain field types "first: StringField, start: DateField"'
		except UserWarning as e:
			message = str(e)
	return render('nest.html', **locals())


@mod_nest.route("/type/add", methods=['GET', 'POST'])
@login_required
def type_edit():
	return type_form('add')


@mod_nest.route("/type/<string:item_type>/edit", methods=['GET', 'POST'])
@login_required
def type_add(item_type):
	return type_form('edit', item_type)