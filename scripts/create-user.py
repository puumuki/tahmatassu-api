 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import argparse, sys, re, json, os, sys, random

#Include tahmatassu-server diretory to path, so servers modules can be imported
working_directory = os.path.dirname(os.path.abspath(__file__))
tahmatassu_directory = os.path.join(working_directory,'..','tahmatassu-server')
sys.path.insert(0, tahmatassu_directory)

from users import UserStorage
from users import User
from users import calculate_hash
from users import load_userstorage
        
def _generate_salt():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

def create_user(username, password):
    file_path = os.path.join(working_directory, '..', 'users.json')
    userstorage = load_userstorage(file_path)

    if username not in userstorage:
        salt = _generate_salt()
        hash = calculate_hash(password+salt)
        user = User({'username' : user_obj,
                     'hash': json_data[user_obj].get('hash'),
                     'salt': json_data[user_obj].get('salt')}
        userstorage.add_user(user)
        userstorage.save()
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
    return parser

def main(argv=sys.argv):
    argparser = create_argparser()
    args = argparser.parse_args(argv[1:])

    if args.username and args.password:
        create_user(args.username, args.password)
    else:
        argparser.print_help()
        

if __name__ == '__main__':
    main()