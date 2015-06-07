from . import *
from .libs import Type


def process(data):
	types = Type.types()
	for type in types:
		type.href = '/nest/item/%s' % type.name
	return locals()