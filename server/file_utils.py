from os import listdir
from os.path import isfile, join

from app import app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config.get('ALLOWED_EXTENSIONS')

def list_allowed_files():
	files = list_files(app.config.get('UPLOAD_DIRECTORY'))
	return filter(allowed_file, files)

def list_files(path):
	return [ f for f in listdir(path) if isfile(join(path,f)) ]