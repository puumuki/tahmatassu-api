 #!/usr/bin/python
 # -*- coding: utf-8 -*-
"""
Simple exception wrapper class for tahmatassu-api
"""
class TassuException(Exception):

	def __init__(self, message, throwable):
		Exception.__init__(self, message)
		self.throwable = throwable