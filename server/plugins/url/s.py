"""

Types

Displays all items types

@author: Alvin Wan
"""

from server.mod_public.libs import URL

path = 'url'
templates = ['partials/urls.html']


def process(data):
	urls =  URL().model().objects().all()
	for url in urls:
		url.label = url.title
		url.href = "/nest/url/edit/"+url.url
	return locals()