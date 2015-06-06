"""

Types

Displays all items types

@author: Alvin Wan
"""

from server.mod_public.libs import Type

path = 'types'
templates = ['partials/types.html']


def process(data):
	types = Type.types()
	for type in types:
		type.href = '/nest/item/%s' % type.name
	return locals()