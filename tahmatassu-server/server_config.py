import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
#Secret key for Flask Cookies
SECRET_KEY =  os.environ.get('SECRET_KEY', None)
LANGUAGE = 'fi'
HOST = '0.0.0.0'
PORT = os.environ.get('PORT', 9001)

#Directory where recipes are stored
RECIPE_DIRECTORY = os.path.join( BASE_PATH, 'recipes')

#File where user password hashes and privileges are stored
USER_STORAGE = os.path.join( BASE_PATH, 'users.json')

#URL used to reference to image files
BASE_URL = "http://localhost:%s/static/img" % ( PORT, )

#Directory where images and other stuff can be loaded, not implementet touch..
UPLOAD_DIRECTORY = os.path.join( BASE_PATH, 'static', 'img')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

MAX_CONTENT_LENGTH = 1024 * 1024

#Directory where recipes are stored
RECIPE_DIRECTORY = os.path.join( BASE_PATH, 'recipes')

#Automatically reload engine on fatal error?
ENGINE_AUTO_RELOAD = True

#Log Server Output to Screen
LOG_SCREEN = True