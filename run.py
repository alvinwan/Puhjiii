# the main Flask application
from server import app, config

if __name__ == "__main__":
	app.run(host=config.HOST, port=config.PORT)