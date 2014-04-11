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

from tahmatassu.recipe import Recipe
from tahmatassu.recipestorage import RecipeStorage
from tahmatassu.tassuexception import TassuException

from localization.utils import msg

from app import app

def is_authenticated():
	return 'username' in session and session['username'] != None

def response(statuscode, key, arguments=None):
	return json.dumps(msg(key, arguments), ensure_ascii=False), statuscode

def authenticate(username, password):	
	user = app.userstorage.get_user(username)
	authenticated = (user and user.authenticate(password))
	app.logger.info(user)
	if authenticated: session['username'] = username
	return authenticated
		
@app.route("/")
def index(recipes=None):
	if not recipes:
		recipes = app.storage.list_titles()	
	return render_template('index.html',
							authenticated=is_authenticated(),
							nav='recipes',
							recipes=recipes)

@app.route("/search", methods=['GET'])
def search_page():
	search = request.args.get(u'search')	
	result = app.storage.wildcard_search(search) if '*' in search else app.storage.fuzzy_search(search)
	app.logger.debug(search)
	return index(recipes=result)
		
@app.route("/login")
def login_page(error=None):	
	return render_template('login.html',
							authenticated=is_authenticated(),
							error=error)

@app.route("/login/<history>")
def login_page_history(history='', error=None):	
	return render_template('login.html',
							history=history,
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

	recipe = app.storage.load(recipe)
	return render_template('edit.html', authenticated=is_authenticated(),
										nav='edit',
										editurl= '/recipe/'+recipe.name.split('.')[0]+'.md',
										filename=recipe.name.split('.')[0],
										markdown=recipe.markdown)

@app.route("/recipe/<recipe>")
def recipe(recipe):
	recipeobj = app.storage.load(recipe)
	markdown = app.markdown.convert(recipeobj.markdown)
	return render_template('recipe.html',authenticated=is_authenticated(),
										 filename=recipeobj.name, 
										 markdown=markdown)

@app.route("/about")
def about():
	return render_template('about.html',nav='about')

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

	if app.storage.delete(recipe):
		return response(key='recipe.delete', statuscode=httpcode.OK)
	else:
		return response(key='recipe.not_deleted', statuscode=httpcode.NOT_FOUND)

@app.route("/api/search/<text>", methods=['GET'])
def search_recipe(text):
	if '*' in text:
		return json.dumps(app.storage.wildcard_search(text))
	else:
		return json.dumps(app.storage.fuzzy_search(text))

@app.route("/api/recipe",  methods=['GET'])
def get_recipe():
	return response(key='ask.recipe.howto',statuscode=httpcode.NOT_AVAILABLE)	

@app.route("/api/recipe/<name>",  methods=['GET'])
def get_load_recipe(name):
	try:	
		return app.storage.load(name).to_json()
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
		app.storage.save(recipe)
		return response(key='recipe.was.saved.succesfully', statuscode=httpcode.OK)
	except KeyError as error:
		app.logger.error(error)
		return response(key='missing.key', arguments=(str(error),), statuscode=httpcode.NOT_AVAILABLE)		
	except ValueError as error:
		app.logger.error(error)
		return response(key='request.is.expecting.json', statuscode=httpcode.NOT_AVAILABLE)
		
@app.route("/api/recipes",  methods=['GET'])
def list_recipes():
	return json.dumps(app.storage.list())

@app.errorhandler(404)
def page_not_found(error):
	app.logger.error(error)	
	return response(key='resource.not.found', statuscode=httpcode.NOT_FOUND)

if __name__ == "__main__":
	app.run(host=app.config.get('HOST', '0.0.0.0'),
			port=app.config.get('PORT', 8080),
			debug=app.config.get('DEBUG', False))