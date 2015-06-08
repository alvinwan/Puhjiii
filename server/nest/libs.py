from server.auth.libs import Allow
from server.plugins.plugin.libs import Plugin


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
			self.user = user
		else:
			self.plugins.append(Plugin('forbidden'))
			
	def load_plugin(self, choice, **kwargs):
		"""
		Loads a plugin
		:param user: user on the system
		:param choice: plugin name
		:param kwargs: parameters
		:return: 
		"""
		plugin = Plugin(plugin=choice, user=self.user, **kwargs).init()
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