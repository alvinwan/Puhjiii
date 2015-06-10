from . import *

def process(data):
	ext = data.path.split('.')[-1]
	try:
		language = {
			'html': 'markup',
		    'py': 'python'
		}[ext]
	except KeyError:
		language = ext
	return {'language': language}
