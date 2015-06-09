from server.plugins.preview.interactive import parse_html, regex_ready_html
import json
import re

whitespace = re.compile('\s+')


def test_page_parse_basic():
	html = regex_ready_html('<h2>{{ title }}</h2><p>{{ copy }}</p>')
	assert html == '<h2>(?P<title>[\S\s]+)<\/h2><p>(?P<copy>[\S\s]+)<\/p>'


def test_page_process_basic():
	template = '<h2>{{ title }}</h2><p>{{ copy }}</p>'
	final = '<h2>Title YO</h2><p>This is some great copy.</p>'
	data, repeatables, templates = parse_html(template=template, html=final)
	assert data['title'] == 'Title YO'
	assert data['copy'] == 'This is some great copy.'
	
	
def test_page_process_partials():
	template = '<header><h1>{{ title }}</h1></header><section><h2>{{ subtitle }}</h2><p>{{ copy }}</p></section>'
	final = '<header><h1>Some Sample</h1></header><section><h2>Subtitle</h2><p>Some lengthy copy.</p></section>'
	partials = json.loads('{"partials":[{"name": "header", "html": "<header><h1>Some Sample</h1></header>"}]}')['partials']
	data, items, templates = parse_html(template=template, html=final, partials=partials)
	
	assert templates[0]['html'].startswith('{% include "public/partials/header.html" %}')
	assert templates[1]['html'] == '<header><h1>Some Sample</h1></header>'
	
	fields = templates[0]['data']
	values = fields.values()
	assert 'Subtitle' in values
	assert 'Some lengthy copy.' in values
	
	
def test_page_process_molds():
	template = '<header><h1>{{ title }}</h1></header><div><h2>{{ name }}</h2><p>{{ copy }}</p></div>'
	final = '<header><h1>No way.</h1></header><div><h2>Hello World</h2><p>It feels great to be alive.</p></div><div><h2>No World</h2><p>It so funny.</p></div>'
	molds = [{"name": "post", "html": "<div><h2>Hello World</h2><p>It feels great to be alive.</p></div>"}]
	data, molds, templates = parse_html(template=template, html=final, molds=molds)

	main = templates[0]['html']
	assert '{% include "public/partials/post.html" %}' in main
	assert '{% for post in posts %}' in main
	
	mold = molds[0]['items']
	item0 = mold[0].values()
	assert 'Hello World' in item0
	assert 'It feels great to be alive.' in item0
	
	item1 = mold[1].values()
	assert 'No World' in item1
	assert 'It so funny.' in item1