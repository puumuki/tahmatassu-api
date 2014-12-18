"""
Tahmatassu Web Server
~~~~~~~~~~~~~~~~~~~~~
Users module hold userinfomation related logic
:copyright: (c) 2014 by Teemu Puukko.
:license: MIT, see LICENSE for more details.
"""
from collections import OrderedDict

def sort_alphabetically_to_dictionary(data):
    """
    Takes a array containing strings, sort each string to dictionary, by using
    string first letter as key and string as the value. Value is stored to a list.
    :param data: list of strings
    :return: dictionary  
    """
    data = sorted(data, key = lambda fileAndTitle: fileAndTitle.title )
    dictionary = OrderedDict()
    letter = ''
    for value in data:
        if value.title[0].upper() != letter:
            letter = value.title[0].upper()
            dictionary[letter] = []
        dictionary[letter].append(value)
    return dictionary