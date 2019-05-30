 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil

from tahmatassu.recipe import Recipe

class TestRecipe(unittest.TestCase):

	def test_creating_recipe(self):		
		recipe = Recipe(name="MusikkaPiirakka.md", 
						markdown="Mustikka Mansikka Piirkka",
						created=None,
						modified=None)

		self.assertEqual("MusikkaPiirakka.md",recipe.name)
		self.assertEqual("Mustikka Mansikka Piirkka",recipe.markdown)
		self.assertIsNotNone(recipe.created, "Creation date should be set to object creation time")
		self.assertIsNotNone(recipe.modified, "modified date should be set to object creation time")

	def test_validating_recipe(self):
		recipe = Recipe(name="MusikkaPiirakka.md", 
						markdown="Mustikka Mansikka Piirkka",
						created=None,
						modified=None)

		self.assertEqual( True, recipe.valid_filename() )
		
		recipe.name = 'MusikkaPiirakka'
		self.assertEqual( False, recipe.valid_filename() )

		recipe.name = 'MusikkaPiirakka.'
		self.assertEqual( False, recipe.valid_filename() )

		self.assertEqual( True, Recipe('1MusikkaPiirakka2.md', '').valid_filename())
		self.assertEqual( True, Recipe('1MusikkaPiirakka2.md', '').valid_filename())
		self.assertEqual( True, Recipe('2MusikkaPiirakka2.md', '').valid_filename())
		self.assertEqual( False, Recipe('.md', '').valid_filename())
		self.assertEqual( True, Recipe('2.md', '').valid_filename())
		self.assertEqual( True, Recipe('äö.md', '').valid_filename())
		self.assertEqual( True, Recipe('a.md', '').valid_filename())
		self.assertEqual( False, Recipe('a.MD', '').valid_filename())

if __name__ == '__main__':
	unittest.main()
