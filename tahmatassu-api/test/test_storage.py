 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil, time

from tahmatassu.recipe import recipes_to_json
from tahmatassu.recipe import Recipe
from tahmatassu.recipestorage import RecipeStorage
from tahmatassu.tassuexception import TassuException

TEST_DIRECTORY = os.path.join("test", "storage")


MARKDOWN = "Mummin kermatortut\n==================\n"\
			"+ 3dl kermaa\n"\
			"+ 1tl leivinjauhetta\n"\
			"+ 6,5dl vehnäjauhoja\n"\
			"+ 250g voita\n"\
			"Kerma vatkataan vaahdoksi. Kuivat aineet sekoitetaan ja sekoitetaan kermanjoukkoon.\n"\
			"Voi vaivataan muiden aineiden jatkoksi.\n"		


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

	def test_load_all(self):
		storage = RecipeStorage(TEST_DIRECTORY);

		storage.save(Recipe('MustikkaPiirakka.md', 'Mustikka\n'))
		storage.save(Recipe('Tortilla.md', 'Tortilla\n'))
		storage.save(Recipe('BologneseKastike.md', 'Bolognesekastike\n'))
		storage.save(Recipe('Pannukakku.md', 'Artillery'))
		storage.save(Recipe('Artillery.md', 'Pannukakku'))

		recipes = storage.load_all()

		self.assertEqual(len(recipes), 5, 'There sould be four recipes stored to directory')

		#In alphabetically sorted order, not by the file name but by the title
		self.assertEqual(recipes[0].name, 'Pannukakku.md')
		self.assertEqual(recipes[1].name, 'BologneseKastike.md')
		self.assertEqual(recipes[2].name, 'MustikkaPiirakka.md')
		self.assertEqual(recipes[3].name, 'Artillery.md')
		self.assertEqual(recipes[4].name, 'Tortilla.md')

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

	def test_storing_backup(self):
		storage = RecipeStorage(TEST_DIRECTORY, backup=True)
		recipe = Recipe('A.md', MARKDOWN)
		storage.save(recipe)
		storage.save(recipe)		
		storage.save(recipe)
		self.assertEqual(2, len(os.listdir(TEST_DIRECTORY)))

	def test_message_list_to_json(self):
		recipes = []
		recipes.append(Recipe('A.md', MARKDOWN))
		recipes.append(Recipe('B.md', MARKDOWN))
		recipes.append(Recipe('C.md', MARKDOWN))
		recipes.append(Recipe('D.md', MARKDOWN))
		recipes.append(Recipe('E.md', MARKDOWN))
		json = recipes_to_json(recipes)
		self.assertIsNotNone(json)

	def test_list_file_history(self):
		storage = RecipeStorage(TEST_DIRECTORY);
		recipe = Recipe('MustikkaPiirakka.md', MARKDOWN)
		storage.save(recipe)
		storage.backup_recipe(recipe)
		time.sleep(1)
		storage.backup_recipe(recipe)
		recipe=storage.load('MustikkaPiirakka.md')
		recipes=storage.history(recipe)
		self.assertEqual(len(recipes),2)

		


if __name__ == '__main__':
	unittest.main()
