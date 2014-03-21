 #!/usr/bin/python
 # -*- coding: utf-8 -*-
class TassuException(Exception):

	def __init__(self, message, throwable):
		Exception.__init__(self, message)
		self.throwable = throwable