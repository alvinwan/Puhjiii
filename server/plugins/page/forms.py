from server.forms import Form, DynamicForm, wtf
from server.auth.libs import File
from wtforms import validators


class PageForm(DynamicForm):
	
	def populate_templates(self):
		self.template.choices = [(f, f) for f in File.s('templates/public', True)]


class AddPageForm(PageForm):
	title_info = 'Titles for each page must be unique.'
	template_info = 'Create the page to then edit the template\'s contents. These ' \
	                'templates not doing it for you? <a href="/nest/code/import">Import' \
	                '</a> or <a href="/nest/code/upload">upload</a> new templates.'
	url_info = 'Likewise, this must also be unique.'
	
	title = wtf.StringField('Page Title')
	template = wtf.SelectField('Template')
	url = wtf.StringField('URL', validators=[validators.required()])


class EditPageForm(PageForm):
	# general_info = 'For text elements, click directly on the element you\'d' \
	#              ' like to edit. elements to see additional options: ' \
	#              '(1) convert into a repeatable item (i.e., courses, posts, merchandise), ' \
	#              '(2) convert into a reusable template partial (i.e., header, footer) or ' \
	#              '(3) edit the HTML directly.'
	template_info = 'If you would like to edit the code for this page, [view templates](/nest/code).'
	
	title = wtf.StringField('Page Title')
	template = wtf.SelectField('Template')
	url = wtf.StringField('URL')