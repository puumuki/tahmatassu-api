from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import jsonify
from flask import url_for
from flask import g
from flask import redirect

from markdown2 import Markdown

from users import UserStorage
from users import User
from users import calculate_hash

import hashlib, json, httpcode, os, logging

from localization.utils import msg
from localization.utils import language

from logging.handlers import RotatingFileHandler
from logging import Formatter

from tahmatassu.recipestorage import RecipeStorage
from middlewares import StreamConsumingMiddleware
import server_config

def create_console_logger_handler():
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	ch.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'))
	return ch

def create_logging_handler(config):
	logging_file = os.path.join( os.path.dirname(__file__), 'logs', 'tahmatassu.log' )   
	file_handler = RotatingFileHandler(logging_file, 
										mode='a', 
										maxBytes=10000, 
										backupCount=4, 
										encoding='utf-8')

	file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'))
	file_handler.setLevel(logging.DEBUG)

	return file_handler

def load_users(userstorage):
	user_json_location =  app.config.get('USER_STORAGE', None)

	if not user_json_location or not os.path.exists(user_json_location):
		app.logger.error("The user.json file don't exist, cannot load user information.")
		app.logger.error("Check README.MD for more information.");
		return;

	try:
		with open(user_json_location, 'r') as json_file:
			json_data = json.load(json_file)

			for user_obj in json_data:
				userstorage.add_user(User({'username' : user_obj,
											'hash': json_data[user_obj].get('hash'),
											'salt': json_data[user_obj].get('salt')}))
	except OSError as error:
		app.logger.error("Some other application uses the user.json file, cannot load user information.")


#Initializing Flask
app = Flask(__name__)
app.config.from_object(server_config)

app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)

app.logger.handlers = []

app.logger.addHandler(create_logging_handler(app.config))
app.logger.addHandler(create_console_logger_handler())

app.userstorage = UserStorage()
load_users(app.userstorage)

app.markdown = Markdown()
app.storage = RecipeStorage(directory=app.config['RECIPE_DIRECTORY'], 
							backup=True, 
							logger=app.logger.info)

#Jinja Context Processor
@app.context_processor
def inject_template_variables():
    return dict(base_path=app.config['BASE_PATH'], upload_directory=app.config['UPLOAD_DIRECTORY'])

@app.context_processor
def file_size_context_processor():
    def file_size( base_url, file_name ):    	    	
    	return os.stat(os.path.join(base_url, file_name)).st_size / 1024
    return dict(file_size=file_size)


#Set server language response language
language(app.config['LANGUAGE'] if 'LANGUAGE' in app.config else 'fi')

app.logger.info('Started tahmatassu application')