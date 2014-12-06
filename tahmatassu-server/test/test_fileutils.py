 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil

import file_utils
import server

class TestServer(unittest.TestCase):

	def test_fileutils(self):
		self.assertEqual(file_utils.file_suffix('tiikerikakku.JPG'),'jpg')
		self.assertEqual(file_utils.file_suffix('kakku.jpg'),'jpg')
		self.assertEqual(file_utils.file_suffix('.jpg'),'jpg')

	def test_fileutils_file_suffix(self):
		file_utils.file_suffix('')
		file_utils.file_suffix('.jpg')

	def test_allowed_extension(self):
		self.assertTrue(file_utils.allowed_file('tiikerikakku.JPG'))
		self.assertTrue(file_utils.allowed_file('tiikerikakku.jpg'))
		self.assertTrue(file_utils.allowed_file('tiikerikakku.png'))
		self.assertTrue(file_utils.allowed_file('tiikerikakku.PNG'))
		self.assertTrue(file_utils.allowed_file('tiikerikakku.GIF'))
		self.assertTrue(file_utils.allowed_file('tiikerikakku.gif'))

	def test_unallowed_extension(self):
		self.assertFalse(file_utils.allowed_file('tiikerikakku'))
		self.assertFalse(file_utils.allowed_file(''))
		self.assertFalse(file_utils.allowed_file('mussutus.txt'))
		self.assertFalse(file_utils.allowed_file('mussutus.sh'))

if __name__ == '__main__':
	unittest.main()
