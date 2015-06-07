from server.forms import Form, DynamicForm, wtf


class AddPageForm(Form):
	title = wtf.StringField('Page Title')
	template = wtf.SelectField('Template')
	url = wtf.StringField('URL')


class EditPageForm(DynamicForm):
	title = wtf.StringField('Page Title')
	template = wtf.SelectField('Template')
	url = wtf.StringField('URL')