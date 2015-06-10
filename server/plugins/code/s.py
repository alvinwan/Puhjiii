from urllib.parse import urlparse
import config
from os import listdir
from os.path import isdir, join, dirname as parent
from flask import url_for
from . import *

requires = ['view_templates']


def process(obj):
	"""
	Fetches all files in the specified path.
	:param path: 
	:return:
	"""
	allowed_roots = ['plugins', 'static', 'templates']
	path = obj.path
	links = []
	path = path or ''
	rel_dir = parent(path) if not isdir(path) else path
	try:
		if len(urlparse(path).scheme) == 0 and len(rel_dir) == 0 or rel_dir.split('/')[0] in allowed_roots:
			abs_path = lambda *rel: join(config.BASE_DIR, 'server', *rel)
			url_path = lambda *rel: join(url_for('nest.code'), *rel)
			if path and len(parent(path)) > 0:
				links.append(dict(
					href=url_path(parent(path)),
					label='parent',
					fa='fa-mail-reply'
				))
			for thing in listdir(abs_path(rel_dir)):
				if (len(rel_dir) > 0 or thing in allowed_roots) \
					and thing[0] != '.':
					file = dict(
						href=url_path(rel_dir, thing),
						label=thing
					)
					if isdir(abs_path(rel_dir, thing)):
						file['href'] += '/'
						file['fa'] = 'fa-folder'
						file['label'] += '/'
					else:
						file['fa'] = 'fa-file-o'
					links.append(file)
	except FileNotFoundError:
		pass
	return dict(links=links)