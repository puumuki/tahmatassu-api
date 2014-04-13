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

import server_config

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

	if not user_json_location or os.path.exists(user_json_location):
		app.logger.warning("The user.json file don't exist, cannot load user information.")
		app.logger.info("Check README.MD for more information.");

	with open(user_json_location, 'r') as json_file:
	    json_data = json.load(json_file)

	    for user_obj in json_data:
			userstorage.add_user(User({'username' : user_obj,
										'hash': json_data[user_obj].get('hash'),
										'salt': json_data[user_obj].get('salt')}))


#Initializing Flask
app = Flask(__name__)
app.config.from_object(server_config)

app.logger.addHandler(create_logging_handler(app.config))

app.userstorage = UserStorage()
load_users(app.userstorage)

app.markdown = Markdown()
app.storage = RecipeStorage(directory=app.config['RECIPE_DIRECTORY'] , backup=True)

#Set server language response language
language(app.config['LANGUAGE'] if 'LANGUAGE' in app.config else 'fi')

app.logger.info('Started tahmatassu application')