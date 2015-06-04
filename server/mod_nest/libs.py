from urllib.parse import urlparse, urljoin
from server.mod_auth.libs import Allow
import config
from os import listdir, environ
from os.path import isdir, join, dirname as parent
	
	
class Nest:
	"""
	Handles Nest functions
	"""
	
	PTS_DIR = 'nest/partials/'
	
	def __init__(self, user, request):
		"""
		Initializes only if Allow.ed
		:param user: current_user
		:param request: Flask request object
		"""
		if Allow.ed(user, 'access_nest'):
			self.request = request
			self.aside = self.section = None
			self.context = {}
		else:
			self.section = 'You are not allowed here.'
	
	def generate_section(self, user, choice, **kwargs):
		"""
		Generates a section based on choice.
		"""
		kwargs['user'] = user
		try:
			plugin = Plugin(choice, **kwargs)
		except KeyError:
			plugin = Plugin('preview', **kwargs)
		self.section = self.include_partial(plugin.partial)
		self.context.update(plugin.context)

	def generate_aside(self, user, choice, **kwargs):
		"""
		Generates an aside based on choice.
		"""
		kwargs['user'] = user
		try:
			plugin = Plugin(choice, **kwargs)
		except KeyError:
			plugin = Plugin('navbar', type='main')
		self.aside = self.include_partial(plugin.partial)
		self.context.update(plugin.context)
	
	def include_partial(self, partial):
		"""
		Generates include for a partial
		:param partial: path to partial template
		"""
		return '{% include "'+self.PTS_DIR+partial+'" %}'
	

class Plugin:

	partial = None
	context = None
	_defaults = {
		'preview': {
			'partial': 'preview.html',
			'process': lambda self: {
				'src': preview(self)
			}
		},
	    'navbar': {
		    'partial': 'navbar.html',
	        'process': lambda self: {
		        'links': [
			        {'href': '/nest/templates', 'label': 'templates'},
			        {'href': '/nest/urls', 'label': 'urls'},
			        {'href': '/nest/items', 'label': 'items'},
			        {'href': '/nest/settings', 'label': 'settings'},
			        {'href': '/logout', 'label': 'logout'}
		        ]
	        }
	    },
	    'navfiles': {
		    'partial': 'navfiles.html',
		    'process': lambda self: nav_files(self)
	    },
	    'types': {
		    'partial': 'types.html',
	        'process': lambda self: types()
	    },
	    'type_add': {
		    'partial': 'type_add.html',
	        'process': lambda self: {}
	    },
	    'item_add': {
		    'partial': 'item_add.html',
	        'process': lambda self: {}
		    
	    },
	    'items': {
		    'partial': 'navitems.html',
	        'process': lambda self: items(self)
	    },
	    'urls': {
		    'partial': 'navurls.html',
	        'process': lambda self: urls()
	    },
	    'url_add': {
		    'partial': 'url_add.html',
		    'process': lambda self: {}
	    }
	}
	
	def __init__(self, plugin, user=None, requires=None, **kwargs):
		"""
		:param plugin: desired plugin
		:param kwargs: kwargs
		"""
		if 'requires' in kwargs.keys() \
			and not Allow.ed(user, requires):
			self.partial = 'forbidden.html'
			self.context = {}
			return
		for k, v in kwargs.items():
			setattr(self, k, v)
		self.load_plugin(plugin)
			
	def load_plugin(self, plugin):
		"""
		:param plugin: the desired plugin
		"""
		self.partial = self._defaults[plugin]['partial']
		self.context = self._defaults[plugin]['process'](self)
			
			
def preview(obj):
	"""
	Adds path prefix, if the string is not a URI
	:param path: candidate path
	:return: new string
	"""
	path, request = obj.path, getattr(obj, 'request', None)
	API = '/nest/api/template'
	if request:
		parse = urlparse(request.url)
		return urljoin(parse.scheme+'://'+parse.netloc, path)
	if len(urlparse(path).scheme) == 0:
		rel_dir = parent(path) if not isdir(path) else path
		abs_path = lambda *rel: join(config.BASE_DIR, 'server/templates', *rel)
		url_path = lambda *rel: join(API, *rel)
		if isdir(abs_path(path)):
			for file in listdir(abs_path(rel_dir)):
				if not isdir(abs_path(rel_dir, file)):
					return url_path(rel_dir, file)
			return url_path('public/index.html')
		return url_path(path)
	return path


def nav_files(obj):
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


from server.mod_public.libs import Type, Item


def types():
	types = Type.types()
	for type in types:
		type.href = '/nest/item/%s' % type.name
	return locals()


def items(obj):
	type, item_type = obj.type, obj.item_type
	items = Item.items(item_type, type=type, raw=True)
	return dict(type=item_type, items=items)

from server.mod_public.libs import URL


def urls():
	urls =  URL().model().objects().all()
	for url in urls:
		url.label = url.title
		url.href = "/nest/url/"+url.url
	return locals()