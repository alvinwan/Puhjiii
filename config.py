import os

get = os.environ.get

# application setup and security
PORT = get('PORT', 5000)
HOST = get('HOST', '0.0.0.0')
HASH_ROUNDS = 2

# database connection
SECRET_KEY = get('SECRET_KEY', 'flask+mongoengine=<3')
DB = get('DB', 'puhjee')

# testing
DEBUG = get('DEBUG', True)

# define application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))