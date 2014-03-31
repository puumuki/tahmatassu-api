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

import hashlib
import json
import httpcode

from localization.utils import msg
from localization.utils import language
from users import users
import server_config

#https://github.com/trentm/python-markdown2
from markdown2 import Markdown

from tahmatassu.recipe import Recipe
from tahmatassu.recipestorage import RecipeStorage
from tahmatassu.tassuexception import TassuException

markdowner = Markdown()

#Initializing Flask
app = Flask(__name__)
app.config.from_object(server_config)

#Set server language response language
language(app.config['LANGUAGE'] if 'LANGUAGE' in app.config else 'fi')

storage = RecipeStorage(directory='recipes')

def is_authenticated():
	return 'username' in session and session['username'] != None

def response(statuscode, key, arguments=None):
	return json.dumps(msg(key, arguments), ensure_ascii=False), statuscode
	
@app.route("/")
def index():	
	return render_template('index.html',
							authenticated=is_authenticated(),
							nav='recipes',
							recipes=storage.list_titles())

	
@app.route("/login")
def login_page():	
	return render_template('login.html',
							authenticated=is_authenticated())

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
										editurl= '/recipe/'+recipe.name,
										filename=recipe.name,
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
		return redirect("/", code=302)
	else:		
		return login_page()
	
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

	try:						
		recipe = Recipe(name=request.json[u'name'], 
						markdown=request.json[u'markdown'])
		storage.save(recipe)
		return response(key='recipe.was.saved.succesfully', statuscode=httpcode.OK)
	except KeyError as error:
		return response(key='missing.key', arguments=(str(error),), statuscode=httpcode.NOT_AVAILABLE)		
	except ValueError as error:		
		return response(key='request.is.expecting.json', statuscode=httpcode.NOT_AVAILABLE)
		
@app.route("/api/recipes",  methods=['GET'])
def list_recipes():
	return json.dumps(storage.list())

@app.errorhandler(404)
def page_not_found(error):	
	return response(key='resource.not.found', statuscode=httpcode.NOT_FOUND)

if __name__ == "__main__":
	app.run(host=app.config['HOST'],
			port=app.config['PORT'],
			debug=True)