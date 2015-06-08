"""

Navigation Bar

This is a simple application for the nest's
navigation bar.

@author: Alvin Wan
"""

from server.plugins.mold.libs import Mold
from flask import url_for

path = 'navbar'


def process(data):
	links = [
		{'href': url_for('nest.pages'), 'label': 'pages'},
		{'href': url_for('nest.plugins'), 'label': 'plugins'}
	]
	for mold in Mold.model.objects().all():
		links.append({'href': url_for('nest.mold', item_mold=mold.name), 'label': mold.name})
	links += [
		{'href': url_for('nest.settings'), 'label': 'settings'},
		{'href': url_for('nest.codes'), 'label': 'code'},
		{'href': url_for('nest.molds'), 'label': 'molds'},
		{'href': url_for('auth.logout'), 'label': 'logout'}
	]
	return dict(
		links=links
	)