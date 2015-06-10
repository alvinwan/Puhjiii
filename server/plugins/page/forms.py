from server.forms import Form, DynamicForm, wtf
from server.auth.libs import File
from wtforms import validators


class PageForm(DynamicForm):
	
	def populate_templates(self):
		self.template.choices = [(f, f) for f in File.s('templates/public')]


class AddPageForm(PageForm):
	title = wtf.StringField('Page Title')
	template = wtf.SelectField('Template')
	url = wtf.StringField('URL', [validators.required()])


class EditPageForm(PageForm):
	title = wtf.StringField('Page Title')
	template = wtf.SelectField('Template')
	url = wtf.StringField('URL')