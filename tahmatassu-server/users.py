"""
Tahmatassu Web Server
~~~~~~~~~~~~~~~~~~~~~
Users module hold userinfomation related logic
:copyright: (c) 2014 by Teemu Puukko.
:license: MIT, see LICENSE for more details.
"""

import hashlib

def calculate_hash(stuff):
	"""
	Calculate sha1 hash sum for given stuff
	:param stuff: stuff to be hashed
	:returns: calculated hash 
	"""
	sha1 = hashlib.sha1()
	sha1.update(stuff)
	return sha1.hexdigest()

class User:
	"""
	User class hold single user information
	"""
	
	def __init__(self, options={}):
		"""
		Constructor
		:param options: keys username, hash and salt
		"""
		self.username = options.get('username')
		self.hash = options.get('hash')
		self.salt = options.get('salt')
		self.authenticated = False

	def authenticate(self, password):
		"""
		Authenticate user object
		:param password:
		:returns: Return True if user is authenticated otherwise False
		"""
		sha1 = hashlib.sha1()
		sha1.update((password+self.salt).encode('utf-8'))	
		password_hash = sha1.hexdigest()
		self.authenticated = password_hash == self.hash
		return self.authenticated		


	def is_authenticated(self):
		"""
		Is user authenticated
		:returns: Return True if user is authenticated otherwise False
		"""
		return self.authenticated


class UserStorage:
	"""
	:class UserStorage: class stores tahmatassu authenticated users 
	"""

	def __init__(self):
		self.users = {}		
			
	def has_user(self, username):
		"""
		Test is user available
		:param username: Name of user
		:returns: True if user is available otherwise False
		"""
		return username in self.users

	def get_user(self, username):
		"""
		Return User object if user is available
		:param username: User username
		:returns: User object or None
		"""
		return self.users.get(username, None)

	def add_user(self, user):
		"""
		Add  user to user storage
		:param user: User object
		"""
		self.users[user.username] = user

