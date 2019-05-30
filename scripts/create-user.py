 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import argparse, sys, re, json, os, sys, random
import string, json, logging

logging.basicConfig(format='%(message)s', level=logging.DEBUG)

#Include tahmatassu-server diretory to path, so servers modules can be imported
working_directory = os.path.dirname(os.path.abspath(__file__))
tahmatassu_directory = os.path.join(working_directory,'..','tahmatassu-server')
sys.path.insert(0, tahmatassu_directory)

from users import UserStorage
from users import User
from users import calculate_hash

def load_userstorage( user_json_location ):
    
    userstorage = UserStorage()

    if not user_json_location or not os.path.exists(user_json_location):
        logging.error("The user.json file don't exist, cannot load user information.", user_json_location)
        logging.error("Check README.MD for more information.")
        return None

    try:
        with open(user_json_location, 'r') as json_file:
            json_data = json.load(json_file)

            for user_obj in json_data:
                userstorage.add_user(User({'username' : user_obj,
                                            'hash': json_data[user_obj].get('hash'),
                                            'salt': json_data[user_obj].get('salt')}))
            return userstorage
    except OSError as error:
        logging.error("Some other application uses the user.json file, cannot load user information.")


def _generate_salt():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def create_user(username, password, path):
    file_path = os.path.join(working_directory, '..', 'tahmatassu-server', 'users.json')
    userstorage = load_userstorage(file_path)

    if not userstorage.has_user(username):
        salt = _generate_salt()
        hash = calculate_hash( (password+salt).encode('utf-8') )
        user = {
            username: {
                'hash': hash,
                'salt': salt,
                'role': 'editor'
            }
        }
        logging.info( json.dumps(user, indent=4, sort_keys=True) )

    else:
        print("Username is already taken, please choose another name")

def is_username_free():
    pass

def validate_password(password):
    return re.match(r"^(?=.*\d).{4,16}$", password)

def validate(username):

    errors = []

    if not is_username_free(username):
        errors.append('Username is allready taken, please use other name')

    if not validate_password():
        errors.append('Password has to be 8 to 16 letters long')

    return errors

def create_argparser():
    parser = argparse.ArgumentParser(description='Lisaa uusi kayttaja')
    parser.add_argument('-u', '--username', dest='username')
    parser.add_argument('-p', '--password', dest='password')        
    parser.add_argument('-s', '--userstoragepath', dest='path')
    return parser

def main(argv=sys.argv):
    argparser = create_argparser()
    args = argparser.parse_args(argv[1:])

    if args.username and args.password:
        create_user(args.username, args.password, args.path)
    else:
        argparser.print_help()
        

if __name__ == '__main__':
    main()