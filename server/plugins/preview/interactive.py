"""

Interactive


"""

import config
from os.path import join
from server.plugins.page.libs import Page
from server.plugins.item.libs import Item
from flask import render_template
import re

from . import *
from . import basic
from .forms import EditPageInteractiveForm
from mongoengine.errors import DoesNotExist


def process(data):
	context = basic.process(data)
	action, path = data.action, context.get('path')
	if path:
		try:
			page = Page(url=path).get()
			template = 'public/%s' % page.template
			defaults = page.info
		except DoesNotExist:
			template = data.template
			item = Item(id=data.item_id).get()
			defaults = dict(course=item)
		rendered = render_template(template, **defaults)
		interactive_form = EditPageInteractiveForm(html=rendered, path=path)
	locals().update(context)
	return locals()


def postprocess(path=None, template=None, html=None, page=None, url=None):
	"""
	At save, the source is processed:
	+ Using the original template, regex match for all groups
	- Determine if document structure has been changed:
		- if so, generate new template and save new data
			- if old template is not used, prompt user to
			  delete it
		+ if not, save all matched data
			- repeat with each included or extended template
			- for each "sub" template, prompt the user
	"""
	if url:
		page = Page(url=url).get()
		path = page.template
	if not template:
		abs_path = join(config.BASE_DIR, 'server/templates/public', path)
		template = open(abs_path).read()
	regex = re.compile(regex_ready_html(template))
	is_new = is_very_diff(template, html, regex)
	if is_new:
		data = {}
	else:
		data = extract_data(regex, html)
	if url:
		page.load(info=data).save()
	return data
	
	
def regex_ready_html(html):
	"""
	Prepare template for regex compilation:
		- Isolate all control structures and search for each
			individually.
		+ Replace all statements with valid regex match groups
	:param html: the source to edit
	:return: html
	"""
	validtag = re.compile('{{\s?(?P<tag>[A-z0-9_]+)\s?}}')
	return validtag.sub(
		'(?P<\g<tag>>[\S\s]+)', 
		html.replace('\n', '\s{0,}')
	).replace('/', '\/')


def extract_data(regex, html):
	"""
	Return dictionary of key, value pairs from regex and source
	:param regex: matching
	:param html: html
	:return: dictionary of data
	"""
	return regex.match(html).groupdict()


def is_very_diff(original, new, regex):
	return False