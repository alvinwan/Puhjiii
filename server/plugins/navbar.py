"""

Navigation Bar

This is a simple application for the nest's
navigation bar.

@author: Alvin Wan
"""

from server.plugins.mold.libs import Mold
from flask import url_for
from flask_login import current_user
from server.auth.libs import Allow

requires = ['access_nest']

path = 'navbar'


def process(data):
	links = []
	components = ['pages', 'plugins', 'settings', 'codes', 'molds']
	
	for component in components:
		if Allow.ed(current_user, 'access_%s' % component):
			links.append({'href': url_for('nest.%s' % component), 'label': component})
	
	if Allow.ed(current_user, 'access_items'):
		for mold in Mold.model.objects().all():
			links.append({'href': url_for('nest.mold', item_mold=mold.name), 'label': mold.name})
	
	links += [
		{'href': url_for('auth.logout'), 'label': 'logout'}
	]
	
	return dict(
		links=links
	)