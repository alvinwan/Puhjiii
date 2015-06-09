from server.auth.libs import Role, User
from server.nest.libs import Plugin
from server.plugins.code.libs import Template
from mongoengine.errors import DoesNotExist
from jinja2.exceptions import TemplateNotFound

roles = [
	('owner', ['access_nest', 'view_templates', 'modify_templates']),
	('manager', ['access_nest', 'view_templates', 'modify_templates']),
	('developer', ['access_nest', 'view_templates', 'modify_templates']),
	('follower', ['access_nest'])
]

plugins = ['code', 'item', 'mold', 'page', 'plugin', 'preview', 'navbar']

public_templates = ['index.html']


def build(args):
	global roles, plugins, public_templates
	for role in roles:
		Role(name=role[0]).load(permissions=role[1]).save()
	for plugin in plugins:
		Plugin(name=plugin).load(is_active=True).save()
	for template in public_templates:
		path = 'public/'+template
		Template(path=path).load(name=template.split('.')[0]).save()
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
		Plugin(name=args.plugin).get().load(is_active=False).save()
		print('Plugin "%s" deactivated.' % args.plugin)
	except AttributeError:
		print('You must specify a plugin using the -p or --plugin flag.')
	except DoesNotExist:
		print('Plugin "%s" not found.' % args.plugin)
		
		
def register(args):
	try:
		template = Template(path=args.path).load(name=args.name).generate_defaults().save()
		print('Template "%s" at "%s" added with %d fields.' % (args.name, args.path, len(template.defaults.keys())))
	except AttributeError:
		print('You must specify both a path using the --path flag and a name using the -t or --template flag.')
	except TemplateNotFound:
		print('Invalid template path. Path must be relatiave to server/templates/ directory.')
		
		
def grant(args):
	try:
		user = User(email=args.email).get()
		role = Role(name=args.role).get()
		user.load(role=role).save()
	except DoesNotExist as e:
		print(e)

import argparse

parser = argparse.ArgumentParser(description='Setup Puhjee with initial database settings')
parser.add_argument('command', choices=['build', 'install', 'activate', 'deactivate', 'register', 'import', 'grant'],
                    help='add default settings to the database (install/activate/deactivate plugin, register/import template)')
parser.add_argument('-p', '--plugin', type=str, help='specify a plugin name')
parser.add_argument('-t', '--template', type=str, help='specify a template name')
parser.add_argument('--path', type=str, help='specify path')
parser.add_argument('-e', '--email', type=str, help='specify user email')
parser.add_argument('-r', '--role', type=str, help='specify name of role')

args = parser.parse_args()
globals()[args.command](args)