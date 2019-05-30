 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil
import utils
import file_utils
import server
from collections import namedtuple

FileAndTitle = namedtuple('FileAndTitle', 'filename title')

data = [FileAndTitle(filename='cassey.md', title='Cassey'), 
        FileAndTitle(filename='carter.md', title='Carter'), 
        FileAndTitle(filename='flora.md', title='Flora'), 
        FileAndTitle(filename='jasmine',title='Jasmine'),
        FileAndTitle(filename='vallie.md',title='Vallie'),
        FileAndTitle(filename='holli.md',title='Holli'),
        FileAndTitle(filename='steven.md',title='Steven'), 
        FileAndTitle(filename='polly.md',title='Polly'),
        FileAndTitle(filename='corney.md',title='Cortney'), 
        FileAndTitle(filename='ji.md',title='Ji'),
        FileAndTitle(filename='sheron.md',title='Sheron'), 
        FileAndTitle(filename='theresa.md',title='Thresa'),
        FileAndTitle(filename='andera.md',title='Andera'), 
        FileAndTitle(filename='aleanse.md',title='Alease'),
        FileAndTitle(filename='annika.md',title='annika'),
        FileAndTitle(filename='desudesu.md', title='')]

class TestServer(unittest.TestCase):

  def test_sort_alphabetically_to_dictionary(self):
    dictionary = utils.sort_alphabetically_to_dictionary(data)
    self.assertSequenceEqual(sorted(dictionary.keys()),['*','A','C','F','H','J', 'P','S' ,'T','V'])

  def test_sort_alphabetically_to_dictionary_2(self):
    dictionary = utils.sort_alphabetically_to_dictionary([])
    self.assertIsNotNone(dictionary)


if __name__ == '__main__':
  unittest.main()
