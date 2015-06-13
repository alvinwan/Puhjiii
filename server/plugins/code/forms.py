from server.forms import Form, wtf


class EditCodeForm(Form):
	path = wtf.StringField()
	code = wtf.TextAreaField()
	
	
class ImportCodeForm(Form):
	path_info = 'Path to your new template. This is relative to the `templates/` directory.'
	html_info = 'Copy and paste in your HTML here. It will be parsed for default content and made available for new pages.'
	
	path = wtf.StringField()
	html = wtf.TextAreaField()
	
	
class UploadCodeForm(Form):
	files_info = 'Select as many files as you like. However, they must all be HTML files.'
	
	files = wtf.FileField()