 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import unittest, os, sys, shutil

from server.users import calculate_hash
from server.users import User
from server.users import UserStorage

class TestServerStorage(unittest.TestCase):

    def test_creating_user(self):
        User({'username':'teemu',
              'salt':'',
              'hash':''})

    def test_create_user_storage(self):
        UserStorage()

    def test_fetching_user_from_storage(self):
        storage = UserStorage()
        storage.add_user(User({'username' : 'teemu',
                    'hash': calculate_hash('test'+'test'),
                    'hash': 'test'}))
        self.assertIsNotNone(storage.get_user('teemu'),'There sould be at least one user at the storage')

    def test_authentication(self):
        user = User({'username':'teemu',              
                      'hash':calculate_hash('testtest'),
                      'salt':'test',})
        self.assertEqual( user.authenticate('test'), True, 'User should be now authenticated succesfully' )

    def test_fail_authentication(self):
        user = User({'username':'teemu',              
                      'hash':calculate_hash('testtest'),
                      'salt':'test',})
        self.assertEqual( user.authenticate('lolo'), False, 'Authentication should fail' )
        user = User({'username':'teemu',              
                      'hash':calculate_hash('testtest'),
                      'salt':'lol',})
        self.assertEqual( user.authenticate('test'), False, 'Authentication should fail' )


if __name__ == '__main__':
    unittest.main()
        