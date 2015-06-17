"""

URL Routes

All routes should follow the following structure:

[type]/[action]/[identifying data]

Additional data that does not fall into those three
categories should be appended as querystrings.
"""
import datetime

import markdown as mkd
from html import unescape
from flask_login import current_user
from flask import render_template, render_template_string, make_response, Markup, redirect, request
from jinja2.exceptions import TemplatesNotFound, TemplateNotFound, UndefinedError
from server.auth.libs import Allow, Alert
from urllib.parse import urlparse


def render(name, mod=None, repeats=0, markdown=False, **context):
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
	context['alert'] = Alert.check()
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
	return render('error.html', message=message)


def redirect_error(message, url=None, class_='notokay'):
	"""
	Returns user to a page and displays an alert there.
	:param message: message
	:param url: redirect url
	:param class_: class for message
	:return: redirect
	"""
	Alert(message, class_).log()
	if not url:
		url = request.path
	return redirect(url)


def filename(name, mod):
	"""
	Fetch filename according to priority.
	:param name: template name
	:return path or None
	"""
	path, prefixes = name, ['', 'puhjiii.', 'partials/', 'partials/puhjiii.']
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
		def helper(*args, **kwargs):
			if not Allow.ed(current_user, permission):
				return redirect(dest)
			return f(*args, **kwargs)
		helper.__name__ = f.__name__
		return helper
	return decorator


def context(nest, **kwargs):
	"""
	Presets for nest context.
	:param nest: the Nest object
	:return: new context object
	"""
	data = {
		'repeats': 1,
		'markdown': False,
		'nest': nest,
		'mod': 'nest'
	}
	data.update(nest.context, **kwargs)
	return data


def break_cache(url):
	parts = urlparse(url)
	append = '?' if len(parts.query) == 0 else '&'
	return url+append+'cache_break='+str(datetime.datetime.now())