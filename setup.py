from server.auth.libs import Role
from server.nest.libs import Plugin
from mongoengine.errors import DoesNotExist

roles = [
	('owner', ['access_nest', 'view_templates', 'modify_templates']),
	('manager', ['access_nest', 'view_templates', 'modify_templates']),
	('developer', ['access_nest', 'view_templates', 'modify_templates']),
	('follower', ['access_nest'])
]

plugins = ['item', 'template', 'type', 'url', 'navbar', 'preview']


def build(args):
	global roles, plugins
	for role in roles:
		Role(name=role[0]).load(permissions=role[1]).save()
	for plugin in plugins:
		Plugin(name=plugin).load(is_active=True).save()
	print('Build complete.')


def install(args):
	if hasattr(args, 'plugin'):
		Plugin(name=args.plugin).load(is_active=True).save()
		print('Plugin "%s" installed. Use "activate [-p plugin]" to activate.' % args.plugin)


def activate(args):
	try:
		plugin = Plugin(name=args.plugin).get().load(is_active=True).save()
		print('Plugin "%s" activated.' % args.plugin)
	except AttributeError:
		print('You must specify a plugin using the -p or --plugin flag.')
	except DoesNotExist:
		print('Plugin "%s" not found.' % args.plugin)


def deactivate(args):
	try:
		plugin = Plugin(name=args.plugin).get().load(is_active=False).save()
		print('Plugin "%s" deactivated.' % args.plugin)
	except AttributeError:
		print('You must specify a plugin using the -p or --plugin flag.')
	except DoesNotExist:
		print('Plugin "%s" not found.' % args.plugin)
		

import argparse

parser = argparse.ArgumentParser(description='Setup Puhjee with initial database settings')
parser.add_argument('command', choices=['build', 'install', 'activate', 'deactivate'],
                    help='add default settings to the database')
parser.add_argument('-p', '--plugin', type=str, help='specify a plugin name')
parser.add_argument('--path', type=str, help='specify path to the plugin files')

args = parser.parse_args()
globals()[args.command](args)