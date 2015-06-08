from flask import request, redirect, url_for
from flask_login import current_user, login_required

from server.views import render, context_preset
from server.nest.views import mod_nest
from server.nest.libs import Nest
from server.plugins.mold.libs import Mold
from .forms import AddMoldForm, EditMoldForm

from mongoengine.errors import NotUniqueError, DoesNotExist


@mod_nest.route("/molds")
@login_required
def molds():
	nst = Nest(current_user, request)
	nst.load_plugin('mold.s')
	nst.load_plugin('preview.basic', path='', request=request)
	return render('nest.html', **context_preset(nst))


def mold_form(action, item_mold=None):
	if action == 'add':
		form = AddMoldForm(request.form)
		mold = Mold()
	else:
		mold = Mold(name=item_mold).get()
		form = EditMoldForm(request.form, data=mold.str_fields().data())
	nst = Nest(current_user, request)
	nst.load_plugin('mold.%s' % action)
	nst.load_plugin('preview.basic', path='', request=request)
	locals().update(context_preset(nst))
	if request.method == 'POST' and form.validate():
		try:
			mold.load(name=form.name.data).add_fields(form.info.data).save()
			if action == 'add':
				return redirect(url_for('nest.molds'))
			else:
				return redirect(url_for('nest.mold', item_mold=mold.name))
		except NotUniqueError:
			message = 'A group of items with that name already exists.'
		except ValueError:
			message = 'Second field should contain fields like "first, last, middle" and may contain field molds "first: StringField, start: DateField"'
		except UserWarning as e:
			message = str(e)
		except DoesNotExist:
			return render('error.html', message='No such mold exists.')
	return render('nest.html', **locals())


@mod_nest.route("/mold/add", methods=['GET', 'POST'])
@login_required
def mold_add():
	return mold_form('add')


@mod_nest.route("/mold/<string:item_mold>/edit", methods=['GET', 'POST'])
@login_required
def mold_edit(item_mold):
	return mold_form('edit', item_mold)

@mod_nest.route("/mold/<string:item_mold>/delete")
@login_required
def mold_delete(item_mold):
	try:
		Mold(name=item_mold).delete()
		return redirect(url_for('nest.molds'))
	except DoesNotExist:
		return render('error.html', message='No such mold exists.')