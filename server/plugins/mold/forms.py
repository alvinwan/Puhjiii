from server.forms import Form, wtf


class AddMoldForm(Form):
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')


class EditMoldForm(Form):
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')