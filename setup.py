from server.mod_auth.models import Role
from server.mod_nest.models import Plugin

roles = [
	('owner', ['access_nest', 'view_templates', 'modify_templates']),
	('manager', ['access_nest', 'view_templates', 'modify_templates']),
	('developer', ['access_nest', 'view_templates', 'modify_templates']),
	('follower', ['access_nest'])
]

plugins = ['item', 'template', 'type', 'url', 'navbar', 'preview']


def build():
	global roles, plugins
	add_roles(prepare_roles(roles))
	activate_plugins(plugins)
	print('Build complete.')


def prepare_roles(roles):
	dicts = []
	for role in roles:
		obj = Role()
		obj.name = role[0]
		obj.permissions = role[1]
		dicts.append(obj)
	return dicts


def add_roles(roles):
	for role in roles:
		Role.objects(name=role.name).modify(
			upsert=True,
			new=True,
			set__name=role.name,
			set__permissions=role.permissions)


def activate_plugins(plugins):
	for plugin in plugins:
		Plugin.objects(name=plugin).modify(
			upsert=True,
		    new=True,
		    set__name=plugin,
		    set__is_active=True)


import argparse

parser = argparse.ArgumentParser(description='Setup Puhjee with initial database settings')
parser.add_argument('command', type=str, choices=['build'],
                    help='add default settings to the database')

args = parser.parse_args()
globals()[args.command]()