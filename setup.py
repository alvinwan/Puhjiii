from server.mod_auth.models import Role

roles = [
	('owner', ['access_nest']),
	('manager', ['access_nest']),
	('developer', ['access_nest']),
	('follower', ['access_nest'])
]


def build():
	global roles
	add_roles(prepare_roles(roles))
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
	Role.objects.insert(roles)

import argparse

parser = argparse.ArgumentParser(description='Setup Puhjee with initial database settings')
parser.add_argument('command', type=str, choices=['build'],
                    help='add default settings to the database')

args = parser.parse_args()
globals()[args.command]()