import markdown as mkd
from html import unescape
from flask_login import current_user
from flask import render_template, render_template_string, make_response, Markup, redirect
from jinja2.exceptions import TemplatesNotFound, TemplateNotFound, UndefinedError
from server.auth.libs import Allow


def render(name, mod=None, repeats=0, markdown=True, **context):
	"""
	Render a template.
	:param name: template
	:param mod: module
	:param context: data to render with
	:return: flask render_template
	"""
	name = filename(name, mod)
	if markdown:
		for k, v in context.items():
			if isinstance(v, str):
				context[k] = Markup(mkd.markdown(v))
	html = render_template(name, **context)
	for i in range(repeats):
		html = render_template_string(unescape(html), **context)
	return make_response(html)


def render_error(message):
	"""
	Returns a custom error page.
	:param message: error message
	:return: response
	"""
	return message


def filename(name, mod):
	"""
	Fetch filename according to priority.
	:param name: template name
	:return path or None
	"""
	path, prefixes = name, ['', 'puhjee.', 'partials/', 'partials/puhjee.']
	for prefix in prefixes:
		try:
			render_template(path)
			return path
		except (TemplatesNotFound, TemplateNotFound):
			path = modded(prefix+name, mod)
		except UndefinedError:
			return path
	return None


def modded(name, mod):
	"""
	Adds mod prefix to the template path.
	:param name: template
	:param mod: module name and prefix
	:return: string path
	"""
	return name if mod is None else mod+'/'+name


def permission_required(permission=None, dest='/'):
	"""
	Decorator for view functions
	Use like so: @permission_required('access_nest')
	Lists are acceptable: @permission_required(['access_nest', 'view_templates'])
	:param permission: string or list of strings
	:param dest: 
	:return: decorator
	"""
	def decorator(f):
		def helper():
			if not Allow.ed(current_user, permission):
				return redirect(dest)
			return f()
		return helper
	return decorator


def context_preset(nest):
	"""
	Presets for nest context.
	:param nest: the Nest object
	:return: new context object
	"""
	context = {
		'repeats': 1,
		'markdown': False,
		'nest': nest,
		'mod': 'nest'
	}
	context.update(nest.context)
	return context