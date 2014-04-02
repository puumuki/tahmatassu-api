 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import os, time, shutil
from recipe import Recipe
from os import listdir
from os.path import isfile, join
from tassuexception import TassuException
import codecs
from collections import namedtuple
from operator import attrgetter
from datetime import datetime

BACKUP_DATEFORMAT = '%Y-%m-%d %H_%M_%S'

"""
RecipeStorage class contains IO-operations
for storing, loading, renaming and listing
recipes.
"""
class RecipeStorage:

	def __init__(self, directory, backup=False):
		self.backup = backup
		self.directory = directory;

	"""
	Return list of file names, sorted alphabetically.
	"""
	def list(self):			
		files = [ f for f in listdir(self.directory) if isfile(join(self.directory,f))]
		files = filter(lambda filename:self._filter_rules(filename), files)
		return sorted(files)

	"""
	Filter rules used to filter out unwanted files from listings.
	"""
	def _filter_rules(self,filename):
		if filename[0] == '.': return False
		if filename.endswith('.md') or filename.endswith('.MD'): return True

	def _backup_date(self):
		return datetime.now().strftime(BACKUP_DATEFORMAT)

	"""
	Return list of tuples containing recipe file name and recipe's titles
	Return [(file name, title)]
	"""
	def list_titles(self):
		names = []
		files =  self.list()

		FileAndTitle = namedtuple('FileAndTitle', 'filename title')

		for file_name in files:
			with codecs.open(os.path.join( self.directory, file_name ), "r", "utf-8") as f:				
				names.append(FileAndTitle(file_name, f.readline()))

		return sorted(names, key=attrgetter('title'))

	"""
	Load a recipe from the storage, return a recipe object. If IOError or OSError is raises
	it is wrapped around TassuException and raised.	
	"""
	def load(self, name):
		try:
			file_path = os.path.join(self.directory, name)			

			#getmtime() and getctime() return value is a number 
			#giving the number of seconds since the epoc
			modified = os.path.getmtime(file_path)
			created = os.path.getctime(file_path)
					
			with codecs.open(file_path, "r", "utf-8") as file:
				data = file.read()
				return Recipe(name=name, 
							  markdown=data, 
							  created=created, 
							  modified=modified)
		except IOError as error:
			msg = 'Could not open file from: %s/%s ' % (self.directory, name)
			raise TassuException(msg, error)
		except OSError as error:
			msg = 'Could not open file from: %s/%s ' % (self.directory, name)
			raise TassuException(msg, error)

	"""
	Rename recipe with given name
	"""
	def rename(self, oldname, newname ):
		os.rename( self.directory + "/" +oldname, 
				   self.directory + "/" +newname)

	"""
	Do not delete file, rename the file by adding dot as prefix to filename.
	After that file is not anymore listed.
	Return True if file was rename
	"""
	def delete(self, name):
		try:
			self.rename(name, "."+name)
			return True
		except OSError as error:
			raise TassuException("Failed to delete/rename file", error)	
	
	"""
	Make a backup copy from recipe, filename is stored like
	this .old.<timestamp>.<recipname>
	"""	
	def backup_recipe( self, recipe ):
		recipe_path = os.path.join(self.directory, recipe.name)		
		backup_name = '.old.%s.%s' % (self._backup_date(),recipe.name)
		copy_path = os.path.join(self.directory, backup_name)
		shutil.copy( recipe_path, copy_path)

	"""
	Stores a recipe object to the storage.
	"""
	def save(self,recipe):
		recipe_path = os.path.join(self.directory, recipe.name)

		if self.backup and os.path.isfile(recipe_path):
			self.backup_recipe(recipe)

		with open(recipe_path, 'w') as file:
			file.write(recipe.markdown.encode('UTF-8'))
		
			
