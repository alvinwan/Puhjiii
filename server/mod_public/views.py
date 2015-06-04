from flask import request, Blueprint
from server.mod_public.libs import Item, URL
from server.views import render
from os.path import join

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
	req = request.args
	if 'page' in req.keys():
		path, itms = Item.items(variable, req['page'], req['per_page'])
	else:
		path, itms = Item.items(variable)
	return render(path, mod='public', **itms)


@mod_public.route("/<string:item_name>/<int:item_id>")
def item(item_name, item_id):
	path, itms = Item.item(item_name, item_id)
	return render(path, mod='public', **itms)