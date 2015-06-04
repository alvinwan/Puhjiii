from wtforms import Form, fields as wtf


class AddTypeForm(Form):
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')


class EditTypeForm(Form):
	pass


class AddItemForm(Form):
	
	@classmethod
	def propagate(cls, fields):
		for k, field in fields.items():
			v = getattr(wtf, field)(k)
			setattr(cls, k, v)
		return cls
	

class AddURLForm(Form):
	title = wtf.StringField('Page Title')
	template = wtf.StringField('Template')
	url = wtf.StringField('URL')