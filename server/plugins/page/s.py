from .libs import Page
from . import *

requires = ['view_pages']

def process(data):
	pages = Page.model.objects().all()
	return locals()