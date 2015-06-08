from server.libs import Puhjee
from server.auth.libs import Allow
from . import models
import config
import importlib


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
		except ImportError as e:
			self.templates.append('puhjee.error.html')
			self.context = {'message': 'No such plugin\nError: %s' % e}
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
			except ImportError as e:
				config.output(' ! Could not load plugin "%s"\n   Error: %s' % (plugin.name, e))