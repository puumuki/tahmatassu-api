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

#Initializing logging
logging_file = os.path.join( os.path.dirname(__file__), 'logs', 'tahmatassu.log' )   
file_handler = RotatingFileHandler(logging_file, 
									mode='a', 
									maxBytes=10000, 
									backupCount=4, 
									encoding='utf-8')

file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)

#Initializing Flask
app = Flask(__name__)
app.config.from_object(server_config)
app.logger.addHandler(file_handler)

markdown = Markdown()
userstorage = UserStorage()

userstorage.add_user(User({'username' : 'teemu',
							'hash': calculate_hash('korvasieni'+'test'),
							'salt': 'test'}))

userstorage.add_user(User({'username' : 'ressu',
							'hash': calculate_hash('korvasieni'+'test'),
							'salt': 'test'}))

storage = RecipeStorage(directory=app.config['RECIPE_DIRECTORY'] , backup=True)

app.userstorage = userstorage
app.markdown = markdown
app.storage = storage

#Set server language response language
language(app.config['LANGUAGE'] if 'LANGUAGE' in app.config else 'fi')

app.logger.info('Started tahmatassu application')