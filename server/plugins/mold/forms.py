from server.forms import Form, wtf


class AddMoldForm(Form):
	name_info = 'Molds can be anything, from posts to merchandise to clubs.'
	info_info = 'Add fields (1) in a comma-separated list, and (2) use colons to indicate list types e.g., title, publish:DateTimeField'
	
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')


class EditMoldForm(Form):
	info_info = 'Warning: Changing these names will cause you lose data. Old data is not fit into new fields.'
	
	name = wtf.StringField('Name')
	info = wtf.StringField('Fields')