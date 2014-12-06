"""
Tahmatassu Web Server
~~~~~~~~~~~~~~~~~~~~~
File upload and listing related utility functions 
:copyright: (c) 2014 by Teemu Puukko.
:license: MIT, see LICENSE for more details.
"""
from os import listdir
from os.path import isfile, join
from app import app

def file_suffix(filename):
	parts = filename.rsplit('.', 1)
	return parts[1].lower() if len(parts) > 1 else ''

def allowed_file(filename):
	"""
	Test is file type supported, testing relays filename suffix
	:param filename
	:return True is file type is supported otherwise False
	"""
	return '.' in filename and file_suffix(filename) in app.config.get('ALLOWED_EXTENSIONS')
	
def list_allowed_files():
	"""
	List files allowed files from UPLOAD_DIRECTORY, unallowed files
	are filtered out.
	:return list containing file names
	"""
	files = list_files(app.config.get('UPLOAD_DIRECTORY'))
	return filter(allowed_file, files)

def list_files(path):
	"""
	List files from given path
	:param path where file are listed
	:return list containing file names
	"""
	return [ f for f in listdir(path) if isfile(join(path,f)) ]

