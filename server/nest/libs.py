from server.auth.libs import Allow
from server.libs import Puhjee
from . import models
import importlib


class Nest:
	"""
	Handles Nest layout and elements
	"""
	
	def __init__(self, user, request):
		"""
		Initializes only if Allow.ed
		:param user: current_user
		:param request: Flask request object
		"""
		self.context = {}
		self.plugins = []
		if Allow.ed(user, 'access_nest'):
			self.request = request
		else:
			self.plugins.append(Plugin('forbidden'))
			
	def load_plugin(self, user, choice, **kwargs):
		"""
		Loads a plugin
		:param user: user on the system
		:param choice: plugin name
		:param kwargs: parameters
		:return: 
		"""
		plugin = Plugin(plugin=choice, user=user, **kwargs).init()
		self.context.update(plugin.context)
		self.plugins.append(plugin)
		return self
	
	@property
	def panels(self, html='%s'):
		"""
		Returns string of includes for all panels.
		:param html: optionally added container HTML
		:return: string
		"""
		return html % ''.join([plugin.panel() for plugin in self.plugins])
	

class Plugin(Puhjee):
	"""
	Handles advanced functionality for Nest and Puhjee
	as a whole
	"""
	
	model = models.Plugin
	context = None
	
	def __init__(self, **kwargs):
		"""
		Initializes plugin
		:param plugin: desired plugin
		:param kwargs: kwargs
		"""
		super().__init__(**kwargs)
		self.templates = []
		self.context = {}
		self.settings = None
			
	def init(self):
		"""
		Load the plugin's functionality.
		:return: itself
		"""
		try:
			self.settings = importlib.import_module(
				'server.plugins.%s' % self.plugin)
			if not Allow.ed(self.user, getattr(self.settings, 'requires', [])):
				self.templates.append('puhjee.error.html')
				self.context = {'message': 'Forbidden'}
				return self
			parts = self.plugin.split('.')
			default = parts[1] if len(parts) > 1 else ''
			self.templates += getattr(
				self.settings, 
				'templates', 
				['%s.html' % (default or 'menu')])
			for i, template in enumerate(self.templates):
				if '/' not in template:
					self.templates[i] = 'plugins/%s/%s' % (self.settings.path, template)
			self.context = self.settings.process(self)
		except ImportError:
			self.templates.append('puhjee.error.html')
			self.context = {'message': 'No such plugin'}
		return self
	
	def panel(self):
		"""
		Return a stringified version of all panels 
		required for plugin
		:return: string
		"""
		return ''.join(['{% include "'+template+'" %}'
		                for template in self.templates])
	
	@staticmethod
	def load_views():
		"""
		Load views from all activated plugins, if they exists
		:return:
		"""
		for plugin in Plugin.model.objects(
			is_active=True).all():
			try:
				importlib.import_module(
					'server.plugins.%s.views' % plugin.name)
			except ImportError:
				pass