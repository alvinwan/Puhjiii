from server.forms import Form, wtf


class EditPageInteractiveForm(Form):
	html = wtf.TextAreaField()
	path = wtf.StringField()
	partials = wtf.TextAreaField()
	molds = wtf.TextAreaField()