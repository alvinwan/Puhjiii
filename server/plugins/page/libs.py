import config
from server.libs import Puhjee
from . import models

from os.path import join
from bs4 import BeautifulSoup, element


class Page(Puhjee):
	
	model = models.Page

	@staticmethod
	def parse(path):
		abs_path = join(config.BASE_DIR, 'server/templates/public', path)
		html = open(abs_path).read()
		soup = BeautifulSoup(html)
		fields = {}
		Page.dfs(soup, fields, 0, 0)
		return fields


	@staticmethod
	def dfs(soup, fields, depth, i):

		if isinstance(soup, element.NavigableString):
			if hasattr(soup, 'text') and len(soup.text) > 0:
				key = 'd%di%d' % (depth, i)
				fields[key] = soup.text
				soup.text = key
		else:
			for i, child in enumerate(soup.children):
				Page.dfs(child, fields, depth + 1, i)