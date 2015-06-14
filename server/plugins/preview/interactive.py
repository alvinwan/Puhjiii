"""

Interactive
Processing differentiates between three different forms
of files:
- templates -- contains all dynamic content and Page object
- partials -- fixed content
- molds -- dynamic content and Mold object

"""
# TODO: make flow easier to follow, abstract relevant parts into libs.py?
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import json
from server.plugins.mold.libs import Mold

from server.plugins.page.libs import Page
from server.plugins.item.libs import Item
from server.plugins.code.libs import Template
from server.auth.libs import File
from flask import render_template, url_for
from flask_login import current_user
import re

from . import *
from . import basic
from .forms import EditPageInteractiveForm
from mongoengine.errors import DoesNotExist


def process(data):
	context = iedit(data)
	action, path = data.action, context.get('path')
	if path:
		try:
			page = Page(url=path).get()
			template = page.template
			defaults = page.info
		except DoesNotExist:
			template = data.template
			item = Item(id=data.item_id).get()
			defaults = dict(course=item)
		rendered = render_template(template, **defaults)
		interactive_form = EditPageInteractiveForm(html=rendered, path=path)
	locals().update(context)
	return locals()


def iedit(data):
	context = basic.process(data)
	parts = urlparse(context['src'])
	path = parts.path if parts.path != '/' else ''
	context['src'] = url_for('nest.iedit', path=path)
	return context

whitespace = re.compile('>\s+<')


def unjsonify(string, default=''):
	if string:
		return json.loads(whitespace.sub('><', string), strict=False)
	else:
		return default


def postprocess(html, template, host, partials='{"partials":[]}', molds='{"molds":[]}'):
	"""
	Postprocessing occurs in three steps:
	- Grab data from the source; generate new templates if needed
	- Save new templates if applicable
	- Save data with the specified object and update template if applicable
	:param template: template object
	:param host: obj that uses the template
	:return: data
	"""
	partials = unjsonify(partials, {'partials': []})['partials']
	molds = unjsonify(molds, {'molds': []})['molds']
	data, molds, templates = parse_html(
		File.read('templates/'+template.path), 
		html, partials, molds, template_path=template.path, template_obj=template)
	if templates:
		first = templates[0]
		process_templates(templates)
		host.load(template=first['path'], info=first['data'])
	else:
		host.load(info=data)
	if molds:
		process_items(molds)
	host.save()
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


def process_templates(templates):
	for template in templates:
		path, html, name = template['path'], template['soup'].prettify(), template['name']
		File.write('templates/'+path, html)
		Template(name=name, path=path, defaults={}).save()


def process_items(molds):
	for mold in molds:
		
		File.write('templates/'+mold['template_path'], mold['template'])
		File.write('templates/'+mold['partial_path'], mold['template'])
		items = mold['items']
		item = mold['items'][0]
		Template(name=mold['name'], path=path, defaults=item).save()
		mold = Mold(name=mold['name']).load(
			partial=mold['partial_path'],
			template=mold['template_path'],
			info={k: 'StringField' for k in item.keys()}
		).save()
		for item in items:
			Item(mold=mold, author=current_user, info=item).save()


def parse_html(template, html, partials=[], molds=[], template_path='', template_obj=None):
	"""
	At save, the source is processed:
	+ Using the original template, regex match for all groups
	- Determine if document structure has been changed:
		+ if so, generate new template and associated data
		+ if not, return new data
			- repeat with each included or extended template
			- for each "sub" template, prompt the user
	"""
	regex = re.compile(regex_ready_html(template))
	is_new = is_very_diff(template, html, regex, partials, molds)
	html, molds = extract_items(html, molds)
	partials = extract_partials(html, partials, template_path)
	if is_new:
		return None, molds, partials
	else:
		return extract_data(regex, html, template_obj) or {}, molds, None


def is_very_diff(original, new, regex, partials, molds):
	"""
	Returns whether or not the new source has any structural changes
	since the original.
	:param original: source
	:param new: source
	:param regex: regex build for original
	:param partials: list of partials sources
	:return: boolean
	"""
	return len(partials) > 0 or len(molds) > 0


def extract_data(regex, html, template):
	"""
	Return dictionary of key, value pairs from regex and source
	:param regex: matching
	:param html: html
	:return: dictionary of data
	"""
	groups = regex.match(html)
	return groups.groupdict() if groups else template.defaults
	
	
def extract_partials(html, partials, template_path):
	"""
	Extract partials, and substitute in includes.
	:param html: source
	:param partials: identified partials
	:param template_path: path to original template
	:return: templates
	"""
	templates = []
	bits = template_path.split('.')
	main = {
		'name': '.'.join(bits[-2:-1])+'-copy',
		'path': '.'.join(bits[:-1])+'-copy.html',
		'html': whitespace.sub('><', html)
	}
	templates.append(main)
	for partial in partials:
		html, path = partial['html'], 'public/partials/%s.html' % partial['name']
		regex = re.compile(html)
		main['html'] = regex.sub('{% include "'+path+'" %}', main['html'])
		templates.append({
			'name': partial['name'],
			'path': path,
			'html': html
		})
	soup, fields = Template.to_defaults(BeautifulSoup(main['html']))
	main['html'] = str(soup)
	main['soup'] = soup
	main['data'] = fields
	return templates


def extract_items(html, molds):
	"""
	Extract molds and perform substitutions:
	- Convert item to template and ready for return.
	- Convert template to regex, and extract all items.
	- Using regex, swap out all items with a for loop.
		- If noncontinuous, for loop is placed at first
		  item.
	:param html: source
	:param molds: identified mold
	:return: items
	"""
	for mold in molds:
		subhtml = mtchtml = mold['html']
		soup, fields = Template.to_defaults(BeautifulSoup(subhtml))
		mold['template'] = soup.prettify()
		for k, v in fields.items():
			mtchtml = mtchtml.replace(v, '[\S\s]+?')
			subhtml = subhtml.replace(v, '(?P<'+k+'>[\S\s]+?)')
		mtchtml = mtchtml.replace('><', '>\s{0,}<')
		subhtml = subhtml.replace('><', '>\s{0,}<')
		mtchtml = '\s{0,}(%s)\s{0,}' % mtchtml
		match = re.compile(mtchtml)
		groups = match.findall(html)
		datum = re.compile(subhtml)
		mold['items'] = items = []
		for group in groups:
			data = datum.search(group)
			items.append(data.groupdict() if data else {})
		name = mold['name']
		partial_path = mold['partial_path'] = 'public/partials/'+name+'.html'
		mold['template_path'] = 'public/'+name+'.html'
		html = match.sub(
			'{% for '+name+' in '+name+'s %}{% include "'+partial_path+'" %}{% endfor %}',
		    html, count=1)
		html = match.sub('', html)
	return html, molds