from . import *

def process(data):
	ext = data.path.split('.')[-1]
	try:
		language = {
			'html': 'markup',
		    'py': 'python',
		    'js': 'javascript'
		}[ext]
	except KeyError:
		language = ext
	return {'language': language}
