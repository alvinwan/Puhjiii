from .libs import Page
from . import *


def process(data):
	pages = Page.model.objects().all()
	return locals()