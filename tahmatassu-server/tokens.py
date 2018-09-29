import uuid
import time
from app import app

TOKEN_LIFE_TIME = 86400

tokens = []

def create():
  token = {
    "id": str(uuid.uuid1()),
    "created": time.time(),
    "lifetime": TOKEN_LIFE_TIME 
  }
  tokens.append( token )
  return token

def is_token_valid( token ):
  tok = next((x for x in tokens if x['id'] == token['id']), None)
  app.logger.error( tok )
  app.logger.error( tokens )
  return tok is not None and (time.time() < tok['created'] + TOKEN_LIFE_TIME)
  

