 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil

from localization.utils import language 
from localization.utils import msg
import server

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
