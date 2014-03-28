#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import jsonify
from flask import url_for

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

def response(statuscode, key, arguments=None):
	return json.dumps(msg(key, arguments), ensure_ascii=False), statuscode
	
@app.route("/")
def index():	
	return render_template('index.html', recipes=storage.list_titles())

@app.route("/edit")
def create_new():		
	return render_template('edit.html', filename='', markdown='')

@app.route("/edit/<recipe>")
def edit(recipe):	
	recipe = storage.load(recipe)
	return render_template('edit.html', filename=recipe.name, 
										markdown=recipe.markdown)


@app.route("/recipe/<recipe>")
def recipe(recipe):
	recipeobj = storage.load(recipe)
	markdown = markdowner.convert(recipeobj.markdown)
	return render_template('recipe.html',filename=recipeobj.name, 
										 markdown=markdown)

@app.route("/about")
def about():
	return render_template('about.html')

@app.route("/login/<username>/<password>", methods=['POST'])
def login(username, password):	
	sha1 = hashlib.sha1()
	sha1.update(password)	
	if username in users and sha1.hexdigest() == users[username]['hash']:
		session['username'] = username
		return response(key='login.granted', statuscode=httpcode.OK)
	else:
		return response(key='login.denied', statuscode=httpcode.ACCESS_DENIED)		
	
@app.route("/logout", methods=['POST'])
def logout():
	session.pop('username',None)
	return "", httpcode.OK

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
	#if session['username'] is None:
	#	return response(key='access.denied', statuscode=httpcode.ACCESS_DENIED)
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