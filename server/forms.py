from wtforms import Form, fields as wtf


class DynamicForm(Form):
	"""
	Wrapper for the default Form class
	"""

	@classmethod
	def propagate(cls, fields, data={}):
		"""
		Generate fields from a dictionary of fields
		:param fields: dictionary of label => field type
		:param data: (optional) existing data
		:return:
		"""
		for k in cls.__dict__.keys():
			setattr(cls, k, None)
		for k, field in fields.items():
			v = getattr(wtf, field)(k, default=data.get(k, None))
			setattr(cls, k, v)
		return cls