 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import os, time, shutil
import codecs
from recipe import Recipe
from os import listdir
from os.path import isfile, join
from tassuexception import TassuException
import codecs, difflib, fnmatch
from collections import namedtuple
from operator import attrgetter
from datetime import datetime

BACKUP_DATEFORMAT = '%Y-%m-%d %H_%M_%S'

FileAndTitle = namedtuple('FileAndTitle', 'filename title')

"""
RecipeStorage class contains IO-operations
for storing, loading, renaming and listing
recipes.
"""
class RecipeStorage:

	def __init__(self, directory, backup=False, logger=None):
		self.backup = backup
		self.directory = directory;

	def _log(self,text):
		if self._logger:
			self._logger(text)
		else:
			print(text)

	def _filter_titles(self, files_and_titles):
		return map((lambda o: o.title), files_and_titles)

	def _sort_by_title(self, files_and_titles):
		return sorted(files_and_titles, key=attrgetter('title'))

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

		for file_name in files:
			try:
				with open(os.path.join( self.directory, file_name ), "r") as f:				
					title = f.readline().decode("utf-8-sig")					
					names.append(FileAndTitle(file_name, title))
			except UnicodeDecodeError as er:				
				self._log("UnicodeDecodeError on %s file, skipping the file")

		return self._sort_by_title(names)

	"""
	Load all recipes from disk and return them in a array of Recipe objects
	"""	
	def load_all(self):
		try:
			recipes = []

			files_and_titles = self.list_titles()
			files_and_titles = self._sort_by_title(files_and_titles)

			for ft in files_and_titles:
				recipe = self.load(ft.filename)
				recipes.append(recipe)

			return recipes

		except IOError as error:
			msg = 'Could not open file from: %s/%s ' % (self.directory, name)
			raise TassuException(msg, error)
		except OSError as error:
			msg = 'Could not open file from: %s/%s ' % (self.directory, name)
			raise TassuException(msg, error)

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



	"""
	Make a fuzzy search to recipes titles.
	@param {string} text search text
	@param {int} n count of results
	@param {int} cutoff search sensivity is value between 0 - 1
	@return {list<FileAndTitle tuple>} 
	"""
	def fuzzy_search(self, text, n=3, cutoff=0.2):
		files_and_titles = self.list_titles()
		titles = self._filter_titles(files_and_titles)
		titles = difflib.get_close_matches(text, titles, n=n, cutoff=cutoff)
		files_and_titles = filter(lambda o: o.title in titles, files_and_titles)
		return self._sort_by_title(files_and_titles)
	
	"""
	Make a wildcard search to recipes titles.
	@param {string} text search text
	@return {list<FileAndTitle tuple>} containing recipes and names
	"""		
	def wildcard_search(self, text):
		files_and_titles = self.list_titles()
		titles = self._filter_titles(files_and_titles)
		titles = fnmatch.filter(titles, text)
		files_and_titles = filter(lambda o: o.title in titles, files_and_titles)
		return self._sort_by_title(files_and_titles)
