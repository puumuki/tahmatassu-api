 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil

from tahmatassu.recipe import Recipe
from tahmatassu.recipestorage import RecipeStorage
from tahmatassu.tassuexception import TassuException

TEST_DIRECTORY = os.path.join("test", "storage")


MARKDOWN = u"Mummin kermatortut\n==================\n"\
			u"+ 3dl kermaa\n"\
			u"+ 1tl leivinjauhetta\n"\
			u"+ 6,5dl vehnäjauhoja\n"\
			u"+ 250g voita\n"\
			u"Kerma vatkataan vaahdoksi. Kuivat aineet sekoitetaan ja sekoitetaan kermanjoukkoon.\n"\
			u"Voi vaivataan muiden aineiden jatkoksi.\n"		


class TestRecipeStorage(unittest.TestCase):

	def setUp(self):
		if not os.path.exists(TEST_DIRECTORY):
			os.makedirs(TEST_DIRECTORY)
		
	def tearDown(self):
		shutil.rmtree(TEST_DIRECTORY)		

	def test_creating_storage(self):
		storage = RecipeStorage(TEST_DIRECTORY);	

	def test_saving_recipe(self):

		storage = RecipeStorage(TEST_DIRECTORY);

		recipe = Recipe('MustikkaPiirakka.md', MARKDOWN)				
		storage.save(recipe)

	def test_renaming(self):
		storage = RecipeStorage(TEST_DIRECTORY);
		storage.save(Recipe('MustikkaPiirakka.md', ''))


	def test_listing(self):
		storage = RecipeStorage(TEST_DIRECTORY);

		storage.save(Recipe('MustikkaPiirakka.md', ''))
		storage.save(Recipe('Tortilla.md', ''))
		storage.save(Recipe('BologneseKastike.md', ''))
		storage.save(Recipe('Pannukakku.md', ''))

		recipe_names = storage.list()

		self.assertEqual(len(recipe_names), 4, 'There sould be four recipes stored to directory')

		#In alphabetically sorted order
		self.assertEqual(recipe_names[0], 'BologneseKastike.md')
		self.assertEqual(recipe_names[1], 'MustikkaPiirakka.md')
		self.assertEqual(recipe_names[2], 'Pannukakku.md')
		self.assertEqual(recipe_names[3], 'Tortilla.md')

	def test_loading_recipe(self):
		storage = RecipeStorage(TEST_DIRECTORY);

		recipe = Recipe('MustikkaPiirakka.md', MARKDOWN)				
		
		storage.save(recipe)
		recipe = storage.load('MustikkaPiirakka.md');

		self.assertEqual(recipe.name, 'MustikkaPiirakka.md','Recipe name should be MustikkaPiirakka.md')
		self.assertIsNotNone(recipe.markdown, 'Recipe should have some markdown on it.')

	def test_loading_recipe(self):
		storage = RecipeStorage(TEST_DIRECTORY);
		recipe = Recipe('MustikkaPiirakka.md', MARKDOWN)						
		storage.save(recipe)

		recipes = storage.list_titles()

		self.assertEqual(1, len(recipes),'There should be at least one recipe at the list')	

	def test_turning_recipe_to_json(self):
		recipe = Recipe('MustikkaPiirakka.MD', 'Lahnaaa....')
		recipe.to_json()

	def test_loading_non_existing_recipe(self):
		storage = RecipeStorage(TEST_DIRECTORY)
		self.assertRaises(TassuException, storage.load, 'EiTallaistaOle.md')		

	def test_filtering(self):
		storage = RecipeStorage(TEST_DIRECTORY)
		recipe = Recipe('A.md', MARKDOWN)
		storage.save(recipe)
		recipe = Recipe('B.md', MARKDOWN)
		recipe = Recipe('B.MD', MARKDOWN)
		storage.save(recipe)
		recipe = Recipe('C.md', MARKDOWN)
		recipe = Recipe('C.txt', MARKDOWN)
		storage.save(recipe)
		recipe = Recipe('.gitignore', MARKDOWN)
		storage.save(recipe)
		recipes = storage.list()
		self.assertNotIn('.gitignore',recipes)
		self.assertNotIn('C.txt',recipes)
		self.assertIn('B.MD',recipes)
		self.assertIn('A.md',recipes)

	def test_deleting(self):
		storage = RecipeStorage(TEST_DIRECTORY)
		recipe = Recipe('A.md', MARKDOWN)
		storage.save(recipe)
		recipe = Recipe('B.md', MARKDOWN)
		storage.save(recipe)
		storage.delete('A.md')
		recipes = storage.list()
		self.assertNotIn('A.md',recipes)

if __name__ == '__main__':
	unittest.main()
