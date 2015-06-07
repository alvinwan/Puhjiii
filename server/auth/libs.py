from server.libs import Puhjee
from . import models

from flask_login import UserMixin


class User(UserMixin, Puhjee):
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
	
	
class Role(Puhjee):
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