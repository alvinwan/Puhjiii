"""
Nest object
"""
	
import os
import flask
from server.models import Role

from bs4 import BeautifulSoup
	
	
class Nest:
	"""
	Handles Nest functions
	"""
	
	def __init__(self, user, request):
		if Allow.ed(user, 'access_nest'):
			self.request = request
			self.section = self.section('default')
			self.aside = self.aside('default')
		else:
			self.section = 'You are not allowed here.'
	
	def content(self, user, choice, **kwargs):
		"""
		Generates a section based on choice.
		"""
		pass

	def sidebar(self, user, choice, **kwargs):
		"""
		Generates an aside based on choice.
		"""
		pass
	
	def render(self, template, **context):
		return flask.render_template(template, **context)
	

class Allow:
	
	@staticmethod
	def ed(user, permission):
		print('ALLOWED? ')
		print(user)
		if user.get_id() is None:
			return False
		role = Role.objects(id=user.role).get()
		return permission in role.permissions


class File:
	"""
	File handling
	"""

	@staticmethod
	def abs_path(relative_path, dct=None):
		"""
		Retrieve the absolute path of a relative path
		"""
		dct = dct if dct is not None else os.path.dirname(__file__)
		name = os.path.join(dct, 'templates/'+relative_path)
		return name

	@staticmethod
	def name(name, fullpath=False):
		"""
		Fetch filename according to priority.
		- If the file exists, use that.
		- If the file does not exist, prepend 'puhjee.' and search
		If it still does not exist, continue prepending and trying strings.
		"""
		pieces = name.split('/')
		if len(pieces) <= 1:
			pieces = File.abs_path(name).split('/')
		prepend, file = '/'.join(pieces[:-1])+'/', pieces[-1]
		path = file
		i = 0
		try:
			while not os.path.isfile(prepend + path):
				path = {
					0: 'puhjee.'+file,
					1: 'partials/'+file,
					2: 'partials/puhjee.'+file
				}[i]
				i += 1
		except KeyError:
			flask.abort(404)
		return path if not fullpath else prepend + path