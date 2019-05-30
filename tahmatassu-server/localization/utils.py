  # -*- coding: utf-8 -*-
import logging
import importlib

translation = translation = importlib.import_module('localization.fi')

DATEFORMAT = '%Y-%m-%d %H:%M:%S'

def language(language):
  global translation	
  translation = importlib.import_module( 'localization.' + language )
  
def msg(key, arguments=None):
  if key in translation.keys and arguments == None:
    return translation.keys[key]
  elif key in translation.keys and arguments != None:
    return translation.keys[key] % arguments
  else:
    return 'Missing translation for key '+key

