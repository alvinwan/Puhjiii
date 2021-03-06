from server.libs import Puhjiii
from . import models
import config
from os.path import join, isdir
from os import listdir, walk

from flask_login import UserMixin
from server import store


class User(UserMixin, Puhjiii):
	"""
	System User
	"""
	
	model = models.User

	def is_active(self):
		"""
		If the user is considered 'active' in application
		:return: boolean
		"""
		return not getattr(self, 'is_suspended', None)

	def is_authenticated(self):
		"""
		Method of checking authentication
		:return: boolean
		"""
		return self.exists()

	def is_anonymous(self):
		"""
		If the user is not logged in
		:return: boolean
		"""
		return not self.exists()

	def get_id(self):
		"""
		ID for the current user object
		:return: str or None
		"""
		return str(self.id) if self.exists() else None
	
	
class Role(Puhjiii):
	"""
	Roles for each user
	"""
	
	model = models.Role


class Allow:
	"""
	Static methods for authorization
	"""

	@staticmethod
	def ed(user, permissions):
		"""
		Handles permissions, checks if user's role has said permission
		:param user: current_user
		:param permission: the string permission name to check for, or a list of all requirements
		:return: boolean
		"""
		if not user or not user.is_authenticated() or not hasattr(user, 'role'):
			return False
		role = Role(id=user.role).get()
		if isinstance(permissions, list):
			return len(
				list(set(permissions) & set(role.permissions))
			) == len(permissions)
		return permissions in role.permissions
	
	
class File:
	"""
	Static methods for file handling
	"""
	
	@staticmethod
	def join(*args):
		"""
		Joins all specified paths together
		:param args: paths
		:return: combined path
		"""
		return join(*args)
	
	@staticmethod
	def rel(rel, *args):
		original = File.join(*args)
		base = File.abs(rel) + '/'
		return original.replace(base, '')
	
	@staticmethod
	def abs(path='', prefix=''):
		"""
		Returns an absolute path using a path relative to server/
		:param prefix: optional prefix
		:param path: relative path
		:return: string path
		"""
		return join(config.BASE_DIR, 'server', prefix, path)
	
	@staticmethod
	def read(path):
		"""
		Reads contents of file at path relative to server/
		:param path: relative path
		:return: contents of file
		"""
		return open(File.abs(path), 'r').read()
	
	@staticmethod
	def write(path, content):
		"""
		Writes content to specified path relative to server/
		:param path: relative path
		:param content: contents of file
		:return: boolean for success
		"""
		return open(File.abs(path), 'w').write(content)
	
	@staticmethod
	def s(path, recursive=False):
		"""
		List all files in the specified directory.
		:param path: relative path
		:return: list
		"""
		base = File.abs(path)
		if isdir(base):
			if recursive:
				matches = []
				for root, dirnames, filenames in walk(base):
					for filename in filenames:
						if filename.endswith('.html'):
							matches.append(File.rel('templates/public', root, filename))
				return matches
			else:
				return [f for f in listdir(base) if not isdir(join(base, f))]
		else:
			return [path]
	
	
class Alert:
	
	def __init__(self, message, class_='notokay', **kwargs):
		self.message = message
		self.class_ = class_
		
	@staticmethod
	def check():
		"""
		Checks for alerts in session
		:return: alert or None
		"""
		if 'alert' in store:
			data = store.get('alert')
			store.delete('alert')
			return Alert(**data)
		
	def log(self):
		"""
		Save alert in session.
		:return: self
		"""
		store.put('alert', {
			'message': self.message, 
			'class_': self.class_
		})
		return self
	
	def __str__(self):
		"""
		Returns the message
		:return: str
		"""
		return self.message