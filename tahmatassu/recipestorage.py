 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import os, time
from recipe import Recipe
from os import listdir
from os.path import isfile, join
from tassuexception import TassuException
import codecs
from collections import namedtuple
from operator import attrgetter

"""
RecipeStorage class contains IO-operations
for storing, loading, renaming and listing
recipes.
"""
class RecipeStorage:

	def __init__(self, directory):
		self.directory = directory;

	def list(self):		
		files = [ f for f in listdir(self.directory) if isfile(join(self.directory,f))]
		return sorted(files)

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
		except WindowsError as error:
			msg = 'Could not open file from: %s/%s ' % (self.directory, name)
			raise TassuException(msg, error)

	def rename(self, oldname, newname ):
		os.rename( self.directory + "/" +oldname, 
				   self.directory + "/" +newname)

	def save(self,recipe):
		with open(self.directory+'/'+recipe.name, 'w') as file:
			file.write(recipe.markdown.encode('UTF-8'))
		
			
