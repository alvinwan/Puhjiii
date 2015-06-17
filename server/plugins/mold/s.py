from . import *
from .libs import Mold
from flask import url_for

requires = ['view_molds']

def process(data):
	molds = Mold.model.objects().all()
	return locals()