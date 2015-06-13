import os

get = os.environ.get

# application setup and security
PORT = get('PORT', 5000)
HOST = get('HOST', '0.0.0.0')
HASH_ROUNDS = 2

# database connection
SECRET_KEY = get('SECRET_KEY', 'flask+mongoengine=<3')
DB = get('DB', 'puhjiii')
SESSION_STORE = 'session'

# testing
DEBUG = get('DEBUG', True)

# define application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# conditional log_level printing
LOG_LEVEL = 0


def output(message, level=1):
	global LOG_LEVEL
	if LOG_LEVEL >= level:
		print(message)