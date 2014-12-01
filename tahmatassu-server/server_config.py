#Server configuration template file.
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

#Turn debug mode on or off, when this is turned on and stacktrace is shown UI
#it is a good idea to turn this off when runnig on production.
DEBUG = True

#This is the secret key that is used to encrypt user session information.
SECRET_KEY = 'testkey'# !!! Replace this with something random !!!

#Server and user interface language
LANGUAGE = 'fi'

#Configures witch interfaces process can be accessed
# all interfaces '0.0.0.0'
# only in localhost '127.0.0.1' or 'localhost'
HOST = '0.0.0.0'
PORT = 8080

#Automatically reload engine on fatal error?
ENGINE_AUTO_RELOAD = True

#Log Server Output to Screen 
LOG_SCREEN = True

#Base URL-that is used to locate the static content
BASE_URL = "http://localhost:8080/static/img"

#Directory where images and other stuff can be loaded, not implementet touch..
UPLOAD_DIRECTORY = os.path.join( BASE_PATH, 'static', 'img')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#Size of maximun file size for uploaded file
MAX_CONTENT_LENGTH = 1024 * 1024

#Directory where recipes are stored
RECIPE_DIRECTORY = os.path.join( BASE_PATH, u'recipes')

#File where user password hashes and privileges are stored
USER_STORAGE = os.path.join( BASE_PATH, u'users.json')

del os
