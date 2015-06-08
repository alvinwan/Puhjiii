from server.plugins.preview.interactive import postprocess, regex_ready_html


def test_page_parse_basic():
	html = regex_ready_html('<h2>{{ title }}</h2><p>{{ copy }}</p>')
	assert html == '<h2>(?P<title>[\S\s]+)<\/h2><p>(?P<copy>[\S\s]+)<\/p>'


def test_page_process_basic():
	template = '<h2>{{ title }}</h2><p>{{ copy }}</p>'
	final = '<h2>Title YO</h2><p>This is some great copy.</p>'
	data = postprocess(template=template, html=final)
	assert data['title'] == 'Title YO'
	assert data['copy'] == 'This is some great copy.'