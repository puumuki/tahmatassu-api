import hashlib, sys, datetime


def main(argv=None):

	if len(argv) < 2:
		print "Give something to hash"

	sha1 = hashlib.sha1()
	sha1.update(argv[1])

	salt = datetime.now().strftime('%s')

	print(sha1.hexdigest())	
	print(salt)

if __name__ == '__main__':
	main(sys.argv)