from flask import render_template
from server.mod_auth.libs import Allow
from flask_login import current_user

from bs4 import BeautifulSoup
	
	
class Nest:
	"""
	Handles Nest functions
	"""
	
	def __init__(self, user, request):
		"""
		Initializes only if Allow.ed
		:param user: current_user
		:param request: Flask request object
		"""
		if Allow.ed(user, 'access_nest'):
			self.request = request
			self.section = self.content(current_user, 'default')
			self.aside = self.sidebar(current_user, 'default')
		else:
			self.section = 'You are not allowed here.'
	
	def content(self, user, choice, **kwargs):
		"""
		Generates a section based on choice.
		"""
		return ''

	def sidebar(self, user, choice, **kwargs):
		"""
		Generates an aside based on choice.
		"""
		return ''
	
	def render(self, template, **context):
		return render_template(template, **context)