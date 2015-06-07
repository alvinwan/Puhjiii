"""

Preview

Allows the user to preview any screen, through an iframe.

@author: Alvin Wan
"""

import config
from os import listdir
from urllib.parse import urlparse, urljoin
from os.path import isdir, join, dirname as parent

path = 'preview'


def process(obj):
	"""
	Adds path prefix, if the string is not a URI
	:param path: candidate path
	:return: new string
	"""
	path, request = obj.path, getattr(obj, 'request', None)
	API = '/nest/api/template'
	if request:
		parse = urlparse(request.url)
		return dict(src=urljoin(parse.scheme+'://'+parse.netloc, path))
	if len(urlparse(path).scheme) == 0:
		rel_dir = parent(path) if not isdir(path) else path
		abs_path = lambda *rel: join(config.BASE_DIR, 'server/templates', *rel)
		url_path = lambda *rel: join(API, *rel)
		if isdir(abs_path(path)):
			for file in listdir(abs_path(rel_dir)):
				if not isdir(abs_path(rel_dir, file)):
					return dict(src=url_path(rel_dir, file))
			return dict(src=url_path('public/index.html'))
		return dict(src=url_path(path))
	return dict(src=path)