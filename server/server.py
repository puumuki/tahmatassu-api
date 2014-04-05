#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import jsonify
from flask import url_for
from flask import g
from flask import redirect

import hashlib, json, httpcode, os, logging

from localization.utils import msg
from localization.utils import language
from users import users
import server_config

from logging.handlers import RotatingFileHandler
from logging import Formatter

from markdown2 import Markdown

from tahmatassu.recipe import Recipe
from tahmatassu.recipestorage import RecipeStorage
from tahmatassu.tassuexception import TassuException

markdowner = Markdown()

#Initializing Flask
app = Flask(__name__)
app.config.from_object(server_config)

logging_file = os.path.join( os.path.dirname(__file__), 'logs', 'tahmatassu.log' )   
file_handler = RotatingFileHandler(logging_file, 
									mode='a', 
									maxBytes=10000, 
									backupCount=4, 
									encoding='utf-8')

file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)

app.logger.addHandler(file_handler)

#Set server language response language
language(app.config['LANGUAGE'] if 'LANGUAGE' in app.config else 'fi')

recipes_directory = os.path.join( os.path.dirname(__file__), 'recipes' )
storage = RecipeStorage(directory=recipes_directory, backup=True)

app.logger.info('Started tahmatassu application')

def is_authenticated():
	return 'username' in session and session['username'] != None

def response(statuscode, key, arguments=None):
	return json.dumps(msg(key, arguments), ensure_ascii=False), statuscode
	
@app.route("/")
def index(recipes=storage.list_titles()):	
	return render_template('index.html',
							authenticated=is_authenticated(),
							nav='recipes',
							recipes=recipes)

@app.route("/search", methods=['GET'])
def search_page():
	search = request.args.get(u'search')	
	result = storage.wildcard_search(search) if '*' in search else storage.fuzzy_search(search)
	app.logger.debug(search)
	return index(recipes=result)
		
@app.route("/login")
def login_page(error=None):	
	return render_template('login.html',
							authenticated=is_authenticated(),
							error=error)

@app.route("/edit")
def create_new():		
	return render_template('edit.html', nav='edit', 
										editurl='/', 
										markdown='')

@app.route("/edit/<recipe>")
def edit(recipe):
	if not is_authenticated():
		return redirect("/recipe/"+recipe, code=302)

	recipe = storage.load(recipe)
	return render_template('edit.html', authenticated=is_authenticated(),
										nav='edit',
										editurl= '/recipe/'+recipe.name.split('.')[0],
										filename=recipe.name.split('.')[0],
										markdown=recipe.markdown)


@app.route("/recipe/<recipe>")
def recipe(recipe):
	recipeobj = storage.load(recipe)
	markdown = markdowner.convert(recipeobj.markdown)
	return render_template('recipe.html',authenticated=is_authenticated(),
										 filename=recipeobj.name, 
										 markdown=markdown)

@app.route("/about")
def about():
	return render_template('about.html',nav='about')

def authenticate(username, password):
	sha1 = hashlib.sha1()
	sha1.update(password)	
	if username in users and sha1.hexdigest() == users[username]['hash']:
		session['username'] = username
		return True
	else:
		return False

@app.route("/api/login", methods=['POST'])
def login():	
	if authenticate(request.form.get('username'),request.form.get('password')):
		app.logger.info('User %s authencated and logged in.' % request.form.get('username'))
		return redirect("/", code=302)
	else:
		app.logger.info('User %s failed to authenticate.' % request.form.get('username'))		
		return login_page(error=True)
	
@app.route("/logout", methods=['POST','GET'])
def logout():
	session.pop('username',None)
	return redirect('/')

@app.route("/api/recipe/<recipe>", methods=['DELETE'])
def delete(recipe):
	if not is_authenticated():
		return response(key='not.authority', statuscode=httpcode.UNAUTHORIZED)

	if storage.delete(recipe):
		return response(key='recipe.delete', statuscode=httpcode.OK)
	else:
		return response(key='recipe.not_deleted', statuscode=httpcode.NOT_FOUND)

@app.route("/api/search/<text>", methods=['GET'])
def search_recipe(text):
	if '*' in text:
		return json.dumps(storage.wildcard_search(text))
	else:
		return json.dumps(storage.fuzzy_search(text))

@app.route("/api/recipe",  methods=['GET'])
def get_recipe():
	return response(key='ask.recipe.howto',statuscode=httpcode.NOT_AVAILABLE)	

@app.route("/api/recipe/<name>",  methods=['GET'])
def get_load_recipe(name):
	try:	
		return storage.load(name).to_json()
	except TassuException as error:		
		return response(key='recipe.not.found', statuscode=httpcode.NOT_FOUND)
	
@app.route("/api/recipe",  methods=['PUT','POST'])
def put_recipe():
	if not is_authenticated():
		return response(key='not.authority', statuscode=httpcode.UNAUTHORIZED)

	app.logger.info( "%s saved a recipe %s " % (session.get('username'), request.json[u'name']))

	try:						
		recipe = Recipe(name=request.json[u'name'], 
						markdown=request.json[u'markdown'])
		storage.save(recipe)
		return response(key='recipe.was.saved.succesfully', statuscode=httpcode.OK)
	except KeyError as error:
		app.logger.error(error)
		return response(key='missing.key', arguments=(str(error),), statuscode=httpcode.NOT_AVAILABLE)		
	except ValueError as error:
		app.logger.error(error)
		return response(key='request.is.expecting.json', statuscode=httpcode.NOT_AVAILABLE)
		
@app.route("/api/recipes",  methods=['GET'])
def list_recipes():
	return json.dumps(storage.list())

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(error)	
	return response(key='resource.not.found', statuscode=httpcode.NOT_FOUND)

if __name__ == "__main__":
	app.run(host=app.config.get('HOST', '0.0.0.0'),
			port=app.config.get('PORT', 8080),
			debug=app.config.get('DEBUG', False))