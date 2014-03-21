  # -*- coding: utf-8 -*-
translation = __import__('fi',globals())	

DATEFORMAT = '%Y-%m-%d %H:%M:%S'

def language(language):
	global translation	
	translation = __import__(language,globals())	

def msg(key, arguments=None):
	if key in translation.keys and arguments == None:
		return translation.keys[key]
	elif key in translation.keys and arguments != None:
		return translation.keys[key] % arguments
	else:
		return 'Missing translation for key '+key

