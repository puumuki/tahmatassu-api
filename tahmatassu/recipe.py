 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from datetime import datetime
import json
import re

DATEFORMAT = '%Y-%m-%d %H:%M:%S'

class Recipe:

	def __init__(self, name, markdown, created=None, modified=None):
		self.name = name
		self.markdown = markdown

		self.created = self._init_datetime(created)
		self.modified = self._init_datetime(modified)

		self.regexp = re.compile("^[\w,\s-]+\.md$",
								re.UNICODE)		

	def _init_datetime(self, time=None):
		return datetime.now() if time == None else datetime.fromtimestamp(int(time))
	
	def valid(self):
		match = self.regexp.match(self.name)
		return match != None		

	def to_json(self):
		return json.dumps({'name':self.name,
							'markdown':self.markdown,
							'created':self.created.strftime(DATEFORMAT),
							'modified':self.modified.strftime(DATEFORMAT)},
							ensure_ascii=False)