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
	def ed(user, permissions):
		"""
		Handles permissions, checks if user's role has said permission
		:param user: current_user
		:param permission: the string permission name to check for, or a list of all requirements
		:return: boolean
		"""
		if not user or \
			not user.is_authenticated() or \
			not hasattr(user, 'role'):
			return False
		role = Role(id=user.role.id).get()
		if isinstance(permissions, list):
			for permission in permissions:
				if permission not in role.permissions:
					return False
			return True
		return permissions in role.permissions