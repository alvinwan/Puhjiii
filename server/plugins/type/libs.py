from . import models
from server.libs import Puhjee
from wtforms import fields as wtf


class Type(Puhjee):
	
	model = models.Type

	@staticmethod
	def types():
		types = []
		for type in Type.model.objects.all():
			types.append(type)
		return types

	def add_fields(self, info):
		fields = {}
		for k in info.split(','):
			if ':' in k:
				k, v = [s.strip() for s in k.split(':')]
				if not hasattr(wtf, v):
					raise UserWarning('No such field')
				fields[k] = v
			else:
				fields[k.strip()] = 'StringField'
		self.info = fields
		return self

	def str_fields(self):
		fields = []
		for k, v in getattr(self, 'info', {}).items():
			if v == 'StringField':
				v = ''
			else:
				v = ': '+v
			fields.append(k+v)
		self.info = ', '.join(fields)
		return self