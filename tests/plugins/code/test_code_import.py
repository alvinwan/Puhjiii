from bs4 import BeautifulSoup
from server.plugins.code.libs import Template


def test_parse_basic():
	html = '<html><div>About</div></html>'
	soup, fields = Template.to_fields(BeautifulSoup(html), prefix=False)
	assert soup.html.div.string == '{{ i0 }}'
	assert len(list(fields.keys())) == 1
	assert fields['i0'] == 'About'


def test_parse_direct_child():
	html = '<html><h2>About<span>Us</span></h2></html>'
	soup, fields = Template.to_fields(BeautifulSoup(html), prefix=False)
	assert soup.html.h2.contents[0] == '{{ i0 }}'
	assert soup.html.h2.span.string == '{{ i1 }}'
	assert len(list(fields.keys())) == 2
	assert fields['i0'] == 'About'
	assert fields['i1'] == 'Us'


def test_parse_dfs_order():
	html = '<html><h2>About<span>Us</span></h2><p>Copy<span>Us</span></p></html>'
	soup, fields = Template.to_fields(BeautifulSoup(html), prefix=False)
	assert soup.html.h2.contents[0] == '{{ i0 }}'
	assert soup.html.h2.span.string == '{{ i1 }}'
	assert soup.html.p.contents[0] == '{{ i2 }}'
	assert soup.html.p.span.string == '{{ i3 }}'
	assert len(list(fields.keys())) == 4
	assert fields['i0'] == 'About'
	assert fields['i1'] == 'Us'
	assert fields['i2'] == 'Copy'
	assert fields['i3'] == 'Us'
	
	
def test_parse_allow_originals():
	html = '<html><h2>{{ title }}</h2></html>'
	soup, fields = Template.to_fields(BeautifulSoup(html), prefix=False)
	assert soup.html.h2.string == '{{ title }}'
	assert fields['title'] == ''
	
	
def test_parse_on_demand():
	html = '<html><h2>About</h2><p>{{ copy }}</html>'
	soup, fields = Template.to_fields(BeautifulSoup(html), prefix=False)
	assert soup.html.h2.string == '{{ i0 }}'
	assert fields['i0'] == 'About'
	assert soup.html.p.string == '{{ copy }}'
	assert fields['copy'] == ''
	
	
def test_generate_defaults_on_demand():
	html = '<html><h2>About</h2><p>{{ copy }}</html>'
	soup, fields = Template.to_defaults(BeautifulSoup(html), prefix=False)
	assert soup.html.h2.string == '{{ i0 }}'
	assert fields['i0'] == 'About'
	assert soup.html.p.string == '{{ copy }}'
	assert fields['copy'] != ''
	
	
def test_replace_only_constants():
	html = '<html><h2>{{ title }}</h2><h3>Copy</h3><p>{{ item.copy }}</p><q>{{ legit_copy }}</q></html>'
	soup, fields = Template.to_fields(BeautifulSoup(html), prefix=False)
	assert soup.html.h2.string == '{{ title }}'
	assert fields['title'] == ''
	assert soup.html.h3.string == '{{ i0 }}'
	assert fields['i0'] == 'Copy'
	assert soup.html.p.string == '{{ item.copy }}'
	assert 'item.copy' not in fields.keys()
	assert soup.html.q.string == '{{ legit_copy }}'
	assert fields['legit_copy'] == ''