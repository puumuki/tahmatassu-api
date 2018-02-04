 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil

from tahmatassu.recipe import Recipe

class TestRecipe(unittest.TestCase):

	def test_creating_recipe(self):		
		recipe = Recipe(name=u"MusikkaPiirakka.md", 
						markdown=u"Mustikka Mansikka Piirkka",
						created=None,
						modified=None)

		self.assertEquals(u"MusikkaPiirakka.md",recipe.name)
		self.assertEquals(u"Mustikka Mansikka Piirkka",recipe.markdown)
		self.assertIsNotNone(recipe.created, "Creation date should be set to object creation time")
		self.assertIsNotNone(recipe.modified, "modified date should be set to object creation time")

	def test_validating_recipe(self):
		recipe = Recipe(name=u"MusikkaPiirakka.md", 
						markdown=u"Mustikka Mansikka Piirkka",
						created=None,
						modified=None)

		self.assertEquals( True, recipe.valid_filename() )
		
		recipe.name = 'MusikkaPiirakka'
		self.assertEquals( False, recipe.valid_filename() )

		recipe.name = 'MusikkaPiirakka.'
		self.assertEquals( False, recipe.valid_filename() )

		self.assertEquals( True, Recipe('1MusikkaPiirakka2.md', '').valid_filename())
		self.assertEquals( True, Recipe('1MusikkaPiirakka2.md', '').valid_filename())
		self.assertEquals( True, Recipe('2MusikkaPiirakka2.md', '').valid_filename())
		self.assertEquals( False, Recipe(u'.md', '').valid_filename())
		self.assertEquals( True, Recipe(u'2.md', '').valid_filename())
		self.assertEquals( True, Recipe(u'äö.md', '').valid_filename())
		self.assertEquals( True, Recipe(u'a.md', '').valid_filename())
		self.assertEquals( False, Recipe(u'a.MD', '').valid_filename())

if __name__ == '__main__':
	unittest.main()
