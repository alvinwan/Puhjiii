from server.forms import Form, wtf

class AddTypeForm(Form):
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')


class EditTypeForm(Form):
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')