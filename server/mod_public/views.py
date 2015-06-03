from flask import request, Blueprint
from server.mod_public.libs import Item
from server.views import render

# setup Blueprint
mod_public = Blueprint('public', __name__)


@mod_public.route("/")
def index():
	return render('index.html', mod='public')

@mod_public.route("/<string:items_name>")
def items(items_name):
	req = request.args
	if 'page' in req.keys():
		path, itms = Item.items(items_name, req['page'], req['per_page'])
	else:
		path, itms = Item.items(items_name)
	return render(path, mod='public', **itms)


@mod_public.route("/<string:item_name>/<int:item_id>")
def item(item_name, item_id):
	path, itms = Item.item(item_name, item_id)
	return render(path, mod='public', **itms)