 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil

from server.localization.utils import language 
from server.localization.utils import msg
from server import server

class TestServer(unittest.TestCase):

	def test_localization(self):
		language('fi')
		self.assertEqual('Missing translation for key ',msg(''))

	def test_existing_localization(self):
		language('fi')
		self.assertEqual(u'Reseptiä ei löytynyt',msg('recipe.not.found'))

	def test_existing_localization_with_arguments(self):
		language('fi')
		self.assertEqual('Tallennus parametri puuttu: testi',msg('missing.key', ('testi',)))

	def test_changing_language(self):
		language('en')
		self.assertEqual('Missing key testi',msg('missing.key', ('testi',)))

if __name__ == '__main__':
	unittest.main()
