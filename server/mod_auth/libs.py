from server.libs import Puhjee

from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin, Puhjee):

	def is_active(self):
		return not self.suspended

	def is_authenticated(self):
		return self.exists()

	def is_anonymous(self):
		return self.exists()

	def get_id(self):
		return str(self.id) if self.exists() else None
	
	
class Role(Puhjee):
	pass


class Allow:

	@staticmethod
	def ed(user, permission):
		"""
		Handles permissions, checks if user's role has said permission
		:param user: current_user
		:param permission: the string permission name to check for
		:return: boolean
		"""
		if not user.is_authenticated() or \
			not hasattr(user, 'role'):
			return False
		role = Role(id=user.role.id).get()
		return permission in role.permissions