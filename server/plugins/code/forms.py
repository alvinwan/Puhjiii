from server.forms import Form, wtf


class EditCodeForm(Form):
	path = wtf.StringField()
	code = wtf.TextAreaField()
	
	
class ImportCodeForm(Form):
	path = wtf.StringField()
	html = wtf.TextAreaField()
	
	
class UploadCodeForm(Form):
	files = wtf.FileField()