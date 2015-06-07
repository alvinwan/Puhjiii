from .libs import Page
from flask import url_for
from . import *


def process(data):
	pages = Page.model.objects().all()
	return locals()