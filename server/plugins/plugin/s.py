from .libs import Plugin
from . import *

requires = ['view_plugins', 'activate_plugin', 'deactivate_plugin']

def process(data):
	plugins = Plugin.model.objects().all()
	return locals()