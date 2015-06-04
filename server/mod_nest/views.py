import config
from flask import request, Blueprint, redirect, make_response, url_for
from flask_login import current_user, login_required

from server.views import render
from server.mod_nest.libs import Nest
from server.mod_auth.libs import Allow
from server.mod_public.libs import Type, Item, URL
from server.mod_public.forms import AddTypeForm, AddItemForm, AddURLForm

from mongoengine.errors import NotUniqueError
from jinja2.exceptions import TemplateNotFound

from os.path import join

# setup Blueprint
mod_nest = Blueprint('nest', __name__, url_prefix='/nest')


def permission_required(permission=None, dest='/'):
	def decorator(f):
		def helper():
			if not Allow.ed(current_user, permission):
				return redirect(dest)
			return f()
		return helper
	return decorator


def mod_preset(nest):
	context = {
		'repeats': 1,
		'markdown': False,
		'nest': nest,
	    'mod': 'nest'
	}
	context.update(nest.context)
	return context


@mod_nest.route("/")
@login_required
# @permission_required('access_nest', '/login')
def home():
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'navbar')
	nst.generate_section(current_user, 'preview', path='', request=request)
	return render('nest.html', **mod_preset(nst))


@mod_nest.route("/templates")
@login_required
def templates():
	return template('public/index.html')


@mod_nest.route("/api/template/")
@mod_nest.route("/api/template/<path:path>")
@mod_nest.route("/api/template/<path:path>/<string:context>", methods=['POST'])
@login_required
def api_template(path='', context={}):
	abs_path = join(config.BASE_DIR, 'server/templates', path)
	if request.method == 'POST':
		return render(path, **context)
	return make_response(open(abs_path).read())
	

@mod_nest.route("/template/")
@mod_nest.route("/template/<path:templt>")
@login_required
def template(templt=''):
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'navfiles', path=templt)
	nst.generate_section(current_user, 'preview', path=templt)
	return render('nest.html', **mod_preset(nst))


@mod_nest.route("/items")
@login_required
def types():
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'types')
	nst.generate_section(current_user, 'preview', path='', request=request)
	return render('nest.html', **mod_preset(nst))


@mod_nest.route("/type/add", methods=['GET', 'POST'])
@login_required
def type_add():
	message=''
	form = AddTypeForm(request.form)
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'type_add')
	nst.generate_section(current_user, 'preview', path='', request=request)
	locals().update(mod_preset(nst))
	if request.method == 'POST' and form.validate():
		try:
			Type(
				name=form.name.data
			).add_fields(form.info.data).save()
			return redirect(url_for('nest.types'))
		except NotUniqueError:
			message = 'A group of items with that name already exists.'
		except ValueError:
			message = 'Second field should contain fields like "first, last, middle" and may contain field types "first: StringField, start: DateField"'
		except UserWarning as e:
			message = str(e)
	return render('nest.html', **locals())


@mod_nest.route("/item/<string:item_type>/<int:item>")
@mod_nest.route("/item/<string:item_type>")
@login_required
def items(item_type, item=None):
	type = Type(name=item_type).get()
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'items', item_type=item_type, type=type)
	nst.generate_section(current_user, 'preview', path='', request=request)
	locals().update(mod_preset(nst))
	return render('nest.html', **locals())


@mod_nest.route("/item/<string:item_type>/add", methods=['GET', 'POST'])
@login_required
def item_add(item_type):
	message=''
	type = Type(name=item_type).get()
	form = AddItemForm.propagate(type.info)
	form = form(request.form)
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'item_add')
	nst.generate_section(current_user, 'preview', path='', request=request)
	locals().update(mod_preset(nst))
	if request.method == 'POST' and form.validate():
		Item(
			info={k: v.data for k, v in form._fields.items()},
			type=type.id).save()
		return redirect("/nest/item/"+item_type)
	return render('nest.html', **locals())


@mod_nest.route("/url/add", methods=['POST', 'GET'])
@login_required
def url_add():
	message=''
	form = AddURLForm(request.form)
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'url_add')
	nst.generate_section(current_user, 'preview', path='', request=request)
	locals().update(mod_preset(nst))
	if request.method == 'POST' and form.validate():
		try:
			render("public/"+form.template.data)
			URL(title=form.title.data,
			    template=form.template.data,
			    url=form.url.data,
			    info=URL.parse(form.template.data)).save()
			return redirect("/nest/urls")
		except (TemplateNotFound, FileNotFoundError):
			message = 'No such template exists.'
	return render('nest.html', **locals())


@mod_nest.route("/urls")
@mod_nest.route("/url/<path:url>")
@login_required
def urls(url=''):
	nst = Nest(current_user, request)
	nst.generate_aside(current_user, 'urls')
	nst.generate_section(current_user, 'preview', path=url, request=request)
	return render('nest.html', **mod_preset(nst))


@mod_nest.route("/settings")
@login_required
def settings():
	return make_response('<a href="/nest">main</a>No settings')