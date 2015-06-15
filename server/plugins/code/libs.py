from os import makedirs
from os.path import exists
from server.libs import Puhjiii
from . import models

from server.auth.libs import File
from bs4 import BeautifulSoup, element
from loremipsum import get_sentence
import re
import string
import random
from werkzeug.utils import secure_filename
from zipfile import ZipFile, is_zipfile


extraneous = re.compile('[\s\S]{0,}<html>([\s\S]+)</html>[\s\S]{0,}')


class Template(Puhjiii):
	
	model = models.Template
	i = 0
	tags = {}

	def __init__(self, **kwargs):
		self.path = None
		self.defaults = {}
		super().__init__(**kwargs)

	@staticmethod
	def soupify(html):
		"""
		Soupify HTML, but removed extraneous code from outside of 
		HTML tags.
		:param html: html
		:return: soup
		"""
		return BeautifulSoup(html.strip())

	@staticmethod
	def stringify(soup):
		"""
		Convert soup back to HTML
		:param soup: soup
		:return: html
		"""
		tags, string = ['link', 'img'], str(soup)
		for tag in tags:
			string = string.replace('</%s>' % tag, '')
			if tag not in Template.tags.keys():
				Template.tags[tag] = re.compile('(<%s[\s\S]{0,}?)/>' % tag)
			string = Template.tags[tag].sub('\g<1>>', string)
		return extraneous.sub('<html>\g<1></html>', string)

	@staticmethod
	def to_template(path):
		"""
		Parses the given source document, generating a Jinja-compatible
		template with associated data
		:param path: path to template file from templates directory
		:return: fields
		"""
		html = File.open(path)
		soup, fields = Template.to_fields(Template.soupify(html))
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
		soup, fields = Template.to_defaults(Template.soupify(html))
		File.write('templates/'+path, Template.stringify(soup))
		return soup, fields

	def import_html(self, html, path=None):
		"""
		Imports the current source or template, by generating and saving
		a new template. Then, it saves this template instance with default
		data.
		:return: self
		"""
		if path:
			self.path = path
		soup, self.defaults = self.import_template(html, self.path)
		return self

	def import_path(self, path):
		"""
		Imports from the specified path.
		:return: self
		"""
		html = File.read('templates/'+path)
		return self.import_html(html, path)
	
	def upload(self, file, path=None, override=True):
		"""
		Upload the given target.
		:return:
		"""
		file.filename = secure_filename(file.filename)
		if is_zipfile(file):
			self.upload_zip(file, path, override)
		else:
			self.upload_file(file, path, override)
		return self

	def upload_file(self, file, path=None, override=True):
		"""
		Upload the given file.
		:param file:
		:param path:
		:return:
		"""
		self.import_html(file.read(), path+file.filename)
		return self
	
	def upload_zip(self, file, path=None, override=True):
		"""
		Upload the zip in three steps:
		1. Extract all files in zipname/ directory.
		2. Move all directories in zipname/ to /static/public/zipname/
		3. Update all links in the files left.
		:param file: 
		:param path: 
		:return:
		"""
		zip = ZipFile(file)
		path = path or File.join('public', file.filename.replace('.zip', ''))
		rel_src = File.join('templates', path)
		rel_dst = File.join('static', path)
		src = File.abs(path, 'templates')
		dst = File.abs(path, 'static')
		
		if not exists(dst):
			makedirs(dst)
		
		moved = []
		for info in zip.infolist():
			name, file = info.filename, File.join(src, info.filename)
			if not name.endswith('.html'):
				zip.extract(info.filename, dst)
				moved.append(info.filename)
			else:
				zip.extract(info.filename, src)
				file_path = '/'.join(File.join(rel_src, info.filename).split('/')[1:])
				Template().import_path(file_path).filter(path=file_path).save()

		for filename in File.s(File.join('templates', path)):
			filepath = File.join('templates', path, filename)
			html = File.read(filepath)
			for dir in moved:
				find, repl = dir, '/' + File.join(rel_dst, dir)
				html = html.replace("'"+find, "'"+repl)
				html = html.replace('"'+find, '"'+repl)
			File.write(filepath, html)
			
		zip.close()
		return self

	def generate_defaults(self):
		"""
		Grabs source and parses for fields. Generates defaults for
		fields that do not have values.
		:return:
		"""
		html = File.read(self.path)
		soup, fields = self.to_defaults(Template.soupify(html))
		self.defaults = fields
		return self