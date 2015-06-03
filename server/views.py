import markdown as mkd
from html import unescape
from flask import render_template, render_template_string, make_response, Markup
from jinja2.exceptions import TemplatesNotFound, TemplateNotFound, UndefinedError


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