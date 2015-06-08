from . import *
from .libs import Item
from flask import url_for


def process(data):
	mold, item_mold = data.mold, data.item_mold
	items = Item.items(item_mold, mold=mold, raw=True)
	return dict(mold=item_mold, items=items)