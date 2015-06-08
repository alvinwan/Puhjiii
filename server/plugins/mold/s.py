from . import *
from .libs import Mold
from flask import url_for


def process(data):
	molds = Mold.model.objects().all()
	return locals()