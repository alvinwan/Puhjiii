from urllib.parse import urlparse
import config
from os import listdir
from os.path import isdir, join, dirname as parent
from . import *

requires = ['view_templates']


def process(obj):
	"""
	Fetches all files in the specified path.
	:param path: 
	:return:
	"""
	path = obj.path
	links = []
	if len(urlparse(path).scheme) == 0:
		path = path or ''
		rel_dir = parent(path) if not isdir(path) else path
		abs_path = lambda *rel: join(config.BASE_DIR, 'server/templates', *rel)
		url_path = lambda *rel: join('/nest/template', *rel)
		if path and len(parent(path)) > 0:
			links.append(dict(
				href=url_path(parent(path)),
				label='parent',
				fa='fa-mail-reply'
			))
		for thing in listdir(abs_path(rel_dir)):
			file = dict(
				href=url_path(rel_dir, thing),
				label=thing
			)
			if isdir(abs_path(rel_dir, thing)):
				file['href'] += '/'
				file['fa'] = 'fa-folder'
			links.append(file)
	return dict(links=links)