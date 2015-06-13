from . import models
from server.libs import Puhjiii
from wtforms import fields as wtf


class Mold(Puhjiii):
	
	model = models.Mold

	def add_fields(self, info):
		fields = {}
		for k in info.split(','):
			k = k.strip()
			if len(k) > 0:
				if ':' in k:
					k, v = [s.strip() for s in k.split(':')]
					if not hasattr(wtf, v):
						raise UserWarning('No such field "%s"' % v)
					fields[k] = v
				else:
					fields[k] = 'StringField'
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