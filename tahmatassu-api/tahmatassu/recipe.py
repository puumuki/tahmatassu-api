 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from datetime import datetime
import json
import re

DATEFORMAT = '%Y-%m-%d %H:%M:%S'


def recipes_to_json(recipes):
	"""
	Array of recipe objects to json
	"""
	data = map(lambda recipe: recipe.to_dictionary(), recipes)
	return json.dumps(data, ensure_ascii=False)


class Recipe:
	"""
	Recipe class contains single recipe information
	"""
	
	def __init__(self, name, markdown, created=None, modified=None):
		"""
		Constructor
		"""
		self.name = name
		self.markdown = markdown
		self.created = self._init_datetime(created)
		self.modified = self._init_datetime(modified)

		self.regexp = re.compile("^[\w,\s-]+\.md$",
								re.UNICODE)		


	def _init_datetime(self, time=None):
		"""
		Return datetime object
		"""
		return datetime.now() if time == None else datetime.fromtimestamp(int(time))
	

	def valid_filename(self):
		"""
		Simple validation for the filename
		"""
		match = self.regexp.match(self.name)
		return match != None		

	def valid_markdown(self):
		return len(self.markdown) > 0


	def to_dictionary(self):
		"""
		Return recipe as a dictionary
		"""
		return {'name':self.name,
				'markdown':self.markdown,
				'created':self.created.strftime(DATEFORMAT),
				'modified':self.modified.strftime(DATEFORMAT)}

	def to_json(self):
		"""
		Return recipe object as JSON string
		"""
		return json.dumps(self.to_dictionary(),
							ensure_ascii=False)

