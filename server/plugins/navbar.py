"""

Navigation Bar

The most basic of plugins. This is a simple application
for the nest's navigation bar.

@author: Alvin Wan
"""

path = 'navbar'
templates = ['partials/navbar.html']


def process(data):
	return dict(
		links=[
			{'href': '/nest/templates', 'label': 'templates'},
			{'href': '/nest/urls', 'label': 'urls'},
			{'href': '/nest/items', 'label': 'items'},
			{'href': '/nest/settings', 'label': 'settings'},
			{'href': '/logout', 'label': 'logout'}
		]
	)