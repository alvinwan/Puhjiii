from wtforms import Form, fields as wtf


class AddTypeForm(Form):
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')


class EditTypeForm(Form):
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')


class DynamicForm(Form):

	@classmethod
	def propagate(cls, fields, data={}):
		for k in cls.__dict__.keys():
			setattr(cls, k, None)
		for k, field in fields.items():
			v = getattr(wtf, field)(k, default=data.get(k, None))
			setattr(cls, k, v)
		return cls


class AddItemForm(DynamicForm):
	pass
	

class EditItemForm(DynamicForm):
	pass


class AddURLForm(Form):
	title = wtf.StringField('Page Title')
	template = wtf.StringField('Template')
	url = wtf.StringField('URL')
	
	
class EditURLForm(DynamicForm):
	title = wtf.StringField('Page Title')
	template = wtf.StringField('Template')
	url = wtf.StringField('URL')