import hashlib

def calculate_hash(stuff):
	sha1 = hashlib.sha1()
	sha1.update(stuff)
	return sha1.hexdigest()

class User:
	
	def __init__(self, options={}):
		self.username = options.get('username')
		self.hash = options.get('hash')
		self.salt = options.get('salt')

	def authenticate(self, password):
		sha1 = hashlib.sha1()
		sha1.update(password+self.salt)
		password_hash = sha1.hexdigest()
		return password_hash == self.hash

class UserStorage:

	def __init__(self):
		self.users = {}		
			

	def has_user(self, username):
		return username in self.users

	def get_user(self, username):
		return self.users.get(username, None)

	def add_user(self, user):
		self.users[user.username] = user

