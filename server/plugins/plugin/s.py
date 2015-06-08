from .libs import Plugin
from . import *


def process(data):
	plugins = Plugin.model.objects().all()
	return locals()