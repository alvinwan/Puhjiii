from server import app
import datetime
from babel.dates import format_timedelta
from markdown import Markdown


md = Markdown()

def timedelta(value, locale='en_US', add_direction=True, **kwargs):
	"""
	Offers a Jinja filter for time deltas.
	:param value: the actual date
	:param locale: default is English US
	:param add_direction: add "ago" or "in"
	:param kwargs: other params
	:return: formatted time difference
	"""
	if isinstance(value, datetime.datetime):
		value = datetime.timedelta(seconds=value.timestamp()-datetime.datetime.now().timestamp())
	return format_timedelta(
		value,
		locale=locale,
		add_direction=add_direction,
		**kwargs)


def markdown(value):
	"""
	Converts a value to valid markdown.
	:param value: actual content
	:return: markdown converted form
	"""
	return md.convert(value)

app.jinja_env.filters['timedelta'] = timedelta
app.jinja_env.filters['markdown'] = markdown