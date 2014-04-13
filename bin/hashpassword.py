import hashlib, sys, datetime, random, string


def generate_randomness(n):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

def main(argv=None):

	if len(argv) < 2:
		print "Give something to hash"

	sha1 = hashlib.sha1()
	salt = generate_randomness(6)

	sha1.update(argv[1] + salt)

	print(sha1.hexdigest())	
	print(salt)

if __name__ == '__main__':
	main(sys.argv)