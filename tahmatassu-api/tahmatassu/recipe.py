 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from datetime import datetime
import json
import re

DATEFORMAT = '%Y-%m-%d %H:%M:%S'

"""
Array of recipe objects to json
"""
def recipes_to_json(recipes):
	data = map(lambda recipe: recipe.to_dictionary(), recipes)
	return json.dumps(data, ensure_ascii=False)

"""
Recipe model object
"""
class Recipe:

	"""
	Constructor
	"""
	def __init__(self, name, markdown, created=None, modified=None):
		self.name = name
		self.markdown = markdown

		self.created = self._init_datetime(created)
		self.modified = self._init_datetime(modified)

		self.regexp = re.compile("^[\w,\s-]+\.md$",
								re.UNICODE)		

	"""
	Return datetime object
	"""
	def _init_datetime(self, time=None):
		return datetime.now() if time == None else datetime.fromtimestamp(int(time))
	
	"""
	Simple validation for the filename
	"""
	def valid(self):
		match = self.regexp.match(self.name)
		return match != None		

	"""
	Return recipe as a dictionary
	"""
	def to_dictionary(self):
		return {'name':self.name,
				'markdown':self.markdown,
				'created':self.created.strftime(DATEFORMAT),
				'modified':self.modified.strftime(DATEFORMAT)}

	"""
	Return recipe object as JSON string
	"""
	def to_json(self):
		return json.dumps(self.to_dictionary(),
							ensure_ascii=False)