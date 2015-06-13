from flask import request, redirect, url_for
from flask_login import current_user, login_required
from server.auth.libs import Alert

from server.views import render, context, redirect_error
from server.nest.views import mod_nest
from server.nest.libs import Nest
from server.plugins.mold.libs import Mold
from .forms import AddMoldForm, EditMoldForm

from mongoengine.errors import NotUniqueError, DoesNotExist


@mod_nest.route("/molds")
@login_required
def molds():
	nest = Nest(current_user, request)
	nest.load_plugin('mold.s')
	nest.load_plugin('preview.basic', path='', request=request)
	return render('nest.html', **context(nest))


def mold_form(form, mold, forward, plugin, error, alert):
	try:
		nest = Nest(current_user, request)
		nest.load_plugin(plugin)
		nest.load_plugin('preview.basic', path='', request=request)
		if request.method == 'POST' and form.validate():
			mold.load(name=form.name.data).add_fields(form.info.data).save()
			alert.log()
			return redirect(forward)
		return render('nest.html', **context(**locals()))
	except NotUniqueError:
		message = 'A group of items with that name already exists.'
	except ValueError:
		message = 'Second field should contain fields like "first, last, middle" and may contain field molds "first: StringField, start: DateField"'
	except (UserWarning, DoesNotExist) as e:
		message = str(e)
	return redirect_error(message, error)


@mod_nest.route("/mold/add", methods=['GET', 'POST'])
@login_required
def mold_add():
	return mold_form(
		form=AddMoldForm(request.form),
		mold=Mold(),
		forward=url_for('nest.molds'),
		plugin='mold.add',
		error=url_for('nest.mold_add'),
		alert=Alert('Mold added.', class_='okay'))


@mod_nest.route("/mold/<string:item_mold>/edit", methods=['GET', 'POST'])
@login_required
def mold_edit(item_mold):
	error=url_for('nest.mold_edit', item_mold=item_mold)
	try:
		mold = Mold(name=item_mold).get()
		return mold_form(
			mold=mold,
			form=EditMoldForm(request.form, data=mold.str_fields().data()),
			forward=url_for('nest.mold', item_mold=mold.name),
			plugin='mold.edit',
			error=error,
			alert=Alert('Mold "%s" updated' % item_mold, class_='okay'))
	except DoesNotExist:
		return redirect_error('No mold "%s" exists.' % item_mold, error)


@mod_nest.route("/mold/<string:item_mold>/delete")
@login_required
def mold_delete(item_mold):
	try:
		Mold(name=item_mold).delete()
		Alert('Mold "%s" deleted.', class_='okay').log()
		return redirect(url_for('nest.molds'))
	except DoesNotExist:
		return redirect_error('No such mold exists.', url_for('nest.molds'))