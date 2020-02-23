#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tahmatassu Web Server
~~~~~~~~~~~~~~~~~~~~~
Main business logic for a web server.
:copyright: (c) 2014 by Teemu Puukko.
:license: MIT, see LICENSE for more details.
"""
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
from tahmatassu.recipe import recipes_to_json
from tahmatassu.recipestorage import RecipeStorage
from tahmatassu.tassuexception import TassuException

from localization.utils import msg

from werkzeug.utils import secure_filename
from werkzeug.wrappers import BaseRequest
from werkzeug.wsgi import responder
from werkzeug.exceptions import RequestEntityTooLarge

import file_utils
import utils
import tokens

from utils import crossdomain

from app import app

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from os import listdir
from os.path import isfile, join


def is_authenticated():
  """
  Test is user authenticated.
  :returns: True if user is authenticated False otherwise
  """
  app.logger.info( "User %s authenticated" % (str(session),) )
  return 'username' in session and session['username'] != None


def response(statuscode, key, arguments=None):
  """
  JSON-response helper
  :param statuscode: http statuscode
  :param key: localization key
  :param arguments:
  :returns: reponse JSON 
  """
  return json.dumps({'message': msg(key, arguments)}, ensure_ascii=False), statuscode

def authenticate(username, password):	
  """
  Autheticate user with username and password using UserStorage.
  If user is authenticated marks username to session object.
  :param username: User username
  :param password: User password
  :returns: True if authenticated otherwise False
  """
  user = app.userstorage.get_user(username)
  authenticated = (user and user.authenticate(password))
  app.logger.info("User %s sign in" % (username,))
  if authenticated: session['username'] = username
  return authenticated

    
@app.before_request
def before_request():
  """
  Executed before each HTTP-request, sets User object to
  request _g_ object if user is authenticated.
  """
  username = session.get('username', '_quest_')		
  g.user = app.userstorage.get_user(username)

@app.route("/")
def index(recipes=None):
  if not recipes:
    recipes = app.storage.list_titles()	
  recipes_dict = utils.sort_alphabetically_to_dictionary(recipes)
  return render_template('index.html',
              user=g.user,							
              recipes=recipes_dict)

@app.route("/search", methods=['GET'])
def search_page():
  search = request.args.get('search')	
  result = app.storage.wildcard_search(search) if '*' in search else app.storage.fuzzy_search(search)
  app.logger.debug(search)
  return index(recipes=result)
    
@app.route("/login")
def login_page(error=None):	
  return render_template('login.html',
              user=g.user,
              history=request.args.get('history',''),
              recipe=request.args.get('recipe',''),
              error=error)

@app.route("/edit")
def create_new():		
  return render_template('edit.html', user=g.user,										 
                    editurl='/', 
                    markdown='',
                    base_url=app.config.get('BASE_URL'),
                    files=file_utils.list_allowed_files())

@app.route("/edit/<recipe>")
def edit(recipe):
  if not is_authenticated():
    return redirect("/recipe/"+recipe, code=302)

  recipe = app.storage.load(recipe)

  return render_template('edit.html', user=g.user,
                    nav='edit',
                    editurl= '/recipe/'+recipe.name.split('.')[0]+'.md',
                    filename=recipe.name.split('.')[0],
                    markdown=recipe.markdown,
                    base_url=app.config.get('BASE_URL'),
                    files=file_utils.list_allowed_files())

@app.route("/recipe/<recipe>")
def recipe(recipe):
  
  
  try:
    recipeobj = app.storage.load(recipe)
    markdown = recipeobj.markdown.replace( app.config.get('PUBLIC_URL') + '/static/img', app.config.get('BASE_URL') )
    markdown = app.markdown.convert(markdown)
    return render_template('recipe.html',user=g.user,
                       filename=recipeobj.name, 
                       markdown=markdown)
  except TassuException as error:
    app.logger.info("Recipe not found")
    return page_not_found(error)

@app.route("/about")
def about():
  return render_template('about.html', user=g.user, nav='about')

@app.route("/api")
def api_page():
  return render_template('api.html', user=g.user, nav='api')

@app.route('/upload', methods=['GET','POST'])
def upload_file():	

  if not is_authenticated():
    return redirect('/')

  if request.method == 'POST':
    file = request.files['file']       

    if file and file_utils.allowed_file(file.filename):
      filename = secure_filename(file.filename)			
      app.logger.debug(os.path.join(app.config.get('UPLOAD_DIRECTORY'), filename))
      file.save(os.path.join(app.config.get('UPLOAD_DIRECTORY'), filename))
      app.logger.debug("Saved")

  files = file_utils.list_allowed_files()	
  return render_template('upload.html', user=g.user, 
                  files=files, 
                  error=request.args.get('error',''),
                  base_url=app.config.get('BASE_URL'))

@app.route("/api/login", methods=['POST','OPTIONS'])
def login():	
  page = '/'+request.form.get('history','index')
  
  if request.form.get('recipe','') != '':
    page += '/' + request.form.get('recipe')	
  
  if authenticate(request.form.get('username'),request.form.get('password')):
    app.logger.info('User %s authencated and logged in.' % request.form.get('username'))
    return redirect(page, code=302)
  else:
    app.logger.info('User %s failed to authenticate.' % request.form.get('username'))		
    return login_page(error=True)
  
@app.route("/logout", methods=['POST','GET'])
def logout():	
  if g.user: app.logger.info("User %s sign out " % (g.user.username,))
  session.pop('username',None)
  page = '/'+request.form.get('history','/')	
  return redirect(page, code=302)

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
  
def save_recipe( name, markdown ):
  try:						
    logging.info(name)
    logging.info(markdown)

    recipe = Recipe(name=name, 
                    markdown=markdown)

    if recipe.valid_filename() and recipe.valid_markdown():
      app.storage.save(recipe)
      return response(key='recipe.was.saved.succesfully', statuscode=httpcode.OK)
    elif not recipe.valid_filename():
      return response(key='recipe.was.save.failed.name.error', statuscode=httpcode.NOT_ACCEPTABLE)
    else:
      return response(key='recipe.was.save.failed.text.too.sort.error', statuscode=httpcode.NOT_ACCEPTABLE)

  except KeyError as error:
    app.logger.error(error)
    return response(key='missing.key', arguments=(str(error),), statuscode=httpcode.NOT_AVAILABLE)		
  except ValueError as error:
    app.logger.error(error)
    return response(key='request.is.expecting.json', statuscode=httpcode.NOT_AVAILABLE)

@app.route("/api/recipe",  methods=['PUT','POST'])
@crossdomain(origin='*')
def put_recipe():
  if not is_authenticated():
    return response(key='not.authority', statuscode=httpcode.UNAUTHORIZED)

  app.logger.info( "%s saved a recipe %s " % (session.get('username'), request.json['name']))
  return save_recipe(name=request.json['name'], markdown=request.json['markdown'])
  


@app.route("/api/v2/recipe",  methods=['PUT','POST','OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def put_recipe_v2():
  if request.json.get('token') and tokens.is_token_valid( request.json.get('token')):
    return save_recipe( request.json.get('name'), request.json.get('markdown') )
  else:
    return response(key='access.denied', statuscode=httpcode.UNAUTHORIZED)

@app.route("/api/files", methods=['GET'])
@crossdomain(origin='*')
def list_all_files():
  path = app.config.get('UPLOAD_DIRECTORY')
  files = [f for f in listdir(path) if isfile(join(path, f))]
  files = map(lambda x: app.config.get('PUBLIC_URL') + app.config.get('PUBLIC_RELATIVE_FILE_URL') +"/"+ x, files )
  return json.dumps( list(files) )
  

@app.route("/api/recipes",  methods=['GET'])
@crossdomain(origin='*')
def list_recipes_only_names():
  try:
    return json.dumps(app.storage.list())
  except TassuException as error:
    app.logger.error(error)
    return json.dumps([])
  

@app.route("/api/v2/recipes",  methods=['GET'])
@crossdomain(origin='*')
def list_recipes_with_content():
  try:
    recipes=[]
    recipe_names = app.storage.list()
    for recipe_name in recipe_names:
      recipes.append(app.storage.load(recipe_name))
    return recipes_to_json(recipes)
  except TassuException as error:
    app.logger.error(error)
    return json.dumps([])
  
@app.route("/api/v2/login", methods=['POST','OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def login_v2():		
  if authenticate(request.json.get('username'), request.json.get('password')):
    return json.dumps({"token": tokens.create()})
  else:
    app.logger.info('User %s failed to authenticate.' % request.form.get('username'))		
    return response(statuscode=httpcode.UNAUTHORIZED, key="access.denied")

@app.route("/api/v2/recipe/<recipe>", methods=['DELETE', 'OPTIONS'])
@crossdomain(origin='*', headers=['Content-Type'])
def delete_v2(recipe):
  if request.json is not None and request.json.get('token') and tokens.is_token_valid( request.json.get('token')):
    if app.storage.delete(recipe):
      return response(key='recipe.delete', statuscode=httpcode.OK)
    else:
      return response(key='recipe.not_deleted', statuscode=httpcode.NOT_FOUND)
  else:
    return response(key='not.authority', statuscode=httpcode.UNAUTHORIZED)


@app.errorhandler(404)
def page_not_found(error):
  """
  Error handler for when page is not found.
  """
  return render_template('page_not_found.html', 
              user=g.user, 
              statuscode=httpcode.NOT_FOUND)

@app.errorhandler(413)
def upload_error(error):
  """
  Error handler for file upload situations.
  """
  app.logger.error(error)	
  return redirect('/upload?error=true')

def server(environ, start_response):
  app.run()

if __name__ == "__main__":
  app.run(host=app.config.get('HOST', '0.0.0.0'),
      port=app.config.get('PORT', ),
      debug=app.config.get('DEBUG', False))