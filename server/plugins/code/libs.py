from server.libs import Puhjiii
from . import models

from server.auth.libs import File
from bs4 import BeautifulSoup, element
from loremipsum import get_sentence
import re
import string
import random


class Template(Puhjiii):
	
	model = models.Template
	i = 0

	def __init__(self, **kwargs):
		self.html = self.path = None
		super().__init__(**kwargs)

	@staticmethod
	def to_template(path):
		"""
		Parses the given source document, generating a Jinja-compatible
		template with associated data
		:param path: path to template file from templates directory
		:return: fields
		"""
		html = File.open(path)
		soup, fields = Template.to_fields(BeautifulSoup(html))
		return soup, fields


	@staticmethod
	def to_fields(soup, prefix=True):
		"""
		Performs a depth-first-search on the document tree. Originally
		implemented dfs directly -> now using BeautifulSoup implementation 
		via "descendants".
		:param soup: BeautifulSoup
		:param fields: optional dictionary
		:return: soup, fields
		"""
		Template.i = 0
		tags = []
		fields = {}
		nonwhitespace = re.compile('\S+')
		validstring = re.compile('{{\s?([A-z0-9_]+)\s?}}')
		validstmt = re.compile('{{\s+\S+\s+}}')
		otherexpr = re.compile('{[^{][\s\S]+[^}]}')
		prefix = ''.join([random.choice(string.ascii_letters) for _ in range(3)]) if prefix else ''
		for child in soup.descendants:
			if isinstance(child, element.NavigableString) \
				and nonwhitespace.search(child):
				tags.append(child)
		for tag in tags:
			match = validstring.match(tag)
			if match:
				key = match.group(1)
				tag = ''
			elif validstmt.match(tag) or otherexpr.match(tag):
				continue
			else:
				key = '%si%d' % (prefix, Template.i)
				tag.replace_with('{{ %s }}' % key)
				Template.i += 1
			fields[key] = tag
		return soup, fields
	
	@staticmethod
	def to_defaults(soup, fields={}, prefix=True):
		"""
		Parses the source soup and generates lorem ipsum for values
		that are blank
		:param soup: BeautifulSoup
		:param fields: initial data
		:return: soup, fields
		"""
		soup, fields = Template.to_fields(soup, prefix)
		for k, v in fields.items():
			if len(v) == 0:
				fields[k] = get_sentence()
		return soup, fields

	@staticmethod
	def import_template(html, path):
		"""
		Parses file and saves generated template in designated
		path.
		:param html: HTML
		:param path: path to save in
		:return: 
		"""
		soup, fields = Template.to_defaults(BeautifulSoup(html))
		File.write('templates/'+path, str(soup))
		return soup, fields

	def import_html(self):
		"""
		Imports the current source or template, by generating and saving
		a new template. Then, it saves this template instance with default
		data.
		:return: self
		"""
		soup, self.defaults = self.import_template(self.html, self.path)
		self.save()
		return self

	def generate_defaults(self):
		"""
		Grabs source and parses for fields. Generates defaults for
		fields that do not have values.
		:return:
		"""
		html = File.read(self.path)
		soup, fields = self.to_defaults(BeautifulSoup(html))
		self.defaults = fields
		return self