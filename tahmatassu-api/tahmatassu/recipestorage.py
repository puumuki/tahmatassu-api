 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import os, time, shutil
import codecs
from .recipe import Recipe
from os import listdir
from os.path import isfile, join
from .tassuexception import TassuException
import codecs, difflib, fnmatch
from collections import namedtuple
from operator import attrgetter
from datetime import datetime
import glob
import ntpath
import re

BACKUP_DATEFORMAT = '%Y-%m-%d %H_%M_%S'

FileAndTitle = namedtuple('FileAndTitle', 'filename title')


class RecipeStorage:
	"""
	RecipeStorage class contains IO-operations
	for storing, loading, renaming and listing
	recipes.
	"""
	def __init__(self, directory, backup=False, logger=None, cache=False):
		self.backup = backup
		self.directory = directory
		self._logger = logger

	def _log(self,text):
		if self._logger:
			self._logger(text)
		else:
			print(text)

	def _filter_titles(self, files_and_titles):
		return list(map((lambda o: o.title), files_and_titles))

	def _sort_by_title(self, files_and_titles):
		return sorted(files_and_titles, key=attrgetter('title'))

	def list(self):			
		"""
		Return list of file names, sorted alphabetically.
		"""
		files = [ f for f in listdir(self.directory) if isfile(join(self.directory,f))]
		files = [filename for filename in files if self._filter_rules(filename)]
		return sorted(files)

	def _filter_rules(self,filename):
		"""
		Filter rules used to filter out unwanted files from listings.
		"""
		if filename[0] == '.': return False
		if filename.endswith('.md') or filename.endswith('.MD'): return True

	def _backup_date(self):
		return datetime.now().strftime(BACKUP_DATEFORMAT)

	def list_titles(self):
		"""
		Return list of tuples containing recipe file name and recipe's titles
		Return [(file name, title)]
		"""
		names = []
		files =  self.list()

		for file_name in files:
			try:
				with open(os.path.join( self.directory, file_name ), "r") as f:				
					title = f.readline().strip()					
					names.append(FileAndTitle(file_name, title))
			except UnicodeDecodeError as er:				
				self._log("UnicodeDecodeError on %s file, skipping the file")

		return self._sort_by_title(names)

	def history(self,recipe):
		"""
		Return recipe's version history as a list. List contains Recipe objects in a
		tronological order.
		@param {Recipe} recipe
		@return list of recipe objects 
		"""
		path = join(self.directory,'.old.*.%s' % (recipe.name))
		files = glob.glob(path)
		file_names = [ntpath.basename(f) for f in files]
		recipes = list(map( self.load, file_names ))
		#map( lambda x: (x.name, x.recipe) , sequence)//Line is not in use
		pattern = r"(.old.)(\d+-\d+-\d+ \d+_\d+_\d+).([A-z]+.md)"
		result = re.compile(pattern).search(recipe.name)
		prefix, date, name = result.groups()
		return sorted( recipes, key=attrgetter('created'))

	def load_all(self):
		"""
		Load all recipes from disk and return them in a array of Recipe objects
		"""
		try:
			recipes = []

			files_and_titles = self.list_titles()
			files_and_titles = self._sort_by_title(files_and_titles)

			for ft in files_and_titles:
				recipe = self.load(ft.filename)
				recipes.append(recipe)

			return recipes

		except IOError as error:
			msg = 'Could not open file from: %s/%s ' % (self.directory,)
			print(error)
			raise TassuException(msg, error)
		except OSError as error:
			msg = 'Could not open file from: %s/%s ' % (self.directory,)
			raise TassuException(msg, error)

	def load(self, name):
		"""
		Load a recipe from the storage, return a recipe object. If IOError or OSError is raises
		it is wrapped around TassuException and raised.	
		"""
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


	def rename(self, oldname, newname ):
		"""
		Rename recipe with given name
		"""
		os.rename( self.directory + "/" +oldname, 
				   self.directory + "/" +newname)

	def delete(self, name):
		"""
		Do not delete file, rename the file by adding dot as prefix to filename.
		After that file is not anymore listed.
		Return True if file was rename
		"""
		try:
			self.rename(name, "."+name)
			return True
		except OSError as error:
			raise TassuException("Failed to delete/rename file", error)	
	
	def backup_recipe( self, recipe ):
		"""
		Make a backup copy from recipe, filename is stored like
		this .old.<timestamp>.<recipname>
		"""
		recipe_path = os.path.join(self.directory, recipe.name)		
		backup_name = '.old.%s.%s' % (self._backup_date(),recipe.name)
		copy_path = os.path.join(self.directory, backup_name)
		shutil.copy( recipe_path, copy_path)

	def save(self,recipe):
		"""
		Stores a recipe object to the storage.
		"""
		recipe_path = os.path.join(self.directory, recipe.name)

		if self.backup and os.path.isfile(recipe_path):
			self.backup_recipe(recipe)

		with open(recipe_path, 'w') as file:
			file.write(recipe.markdown)

	def fuzzy_search(self, text, n=3, cutoff=0.2):
		"""
		Make a fuzzy search to recipes titles.
		@param {string} text search text
		@param {int} n count of results
		@param {int} cutoff search sensivity is value between 0 - 1
		@return {list<FileAndTitle tuple>} 
		"""
		files_and_titles = self.list_titles()
		titles = self._filter_titles(files_and_titles)
		titles = difflib.get_close_matches(text, titles, n=n, cutoff=cutoff)
		files_and_titles = [o for o in files_and_titles if o.title in titles]
		return self._sort_by_title(files_and_titles)
		
	def wildcard_search(self, text):
		"""
		Make a wildcard search to recipes titles.
		@param {string} text search text
		@return {list<FileAndTitle tuple>} containing recipes and names
		"""
		files_and_titles = self.list_titles()
		titles = self._filter_titles(files_and_titles)
		titles = fnmatch.filter(titles, text)
		files_and_titles = [o for o in files_and_titles if o.title in titles]
		return self._sort_by_title(files_and_titles)
