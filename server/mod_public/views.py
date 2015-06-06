from flask import request, Blueprint
from server.mod_public.libs import Item, URL
from server.views import render, render_error
from os.path import join

from jinja2.exceptions import TemplateNotFound, TemplatesNotFound

# setup Blueprint
mod_public = Blueprint('public', __name__)

for url in URL().model().objects().all():
	mod_public.add_url_rule(
		join('/', url.url),
		url.title,
		lambda: render(url.template, mod='public', **url.info))

@mod_public.route("/")
def index():
	return render('index.html', mod='public', person='Bob')

@mod_public.route("/<string:variable>")
def items(variable):
	try:
		req = request.args
		if req.get('id', None):
			return item(variable, None)
		path, itms = Item.items(variable, page=req.get('page', 1), per_page=req.get('per_page', 10))
		return render(path, mod='public', **itms)
	except (TemplatesNotFound, TemplateNotFound):
		return render_error('Template not found for page type.')


@mod_public.route("/<string:item_name>/<string:item_slug>")
def item(item_name, item_slug):
	path, itms = Item.item(
		item_name, 
		item_id=request.args.get('id', None), 
		item_slug=item_slug)
	return render(path, mod='public', **itms)