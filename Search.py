import json
import os
#from curses.ascii import isalpha

from pip._vendor.distlib.compat import raw_input


""""--------------------------------------------------------------------------------------------------------------------
Load functions
---------------------------------------------------------------------------------------------------------------------"""

def file_exists(path, filename):
    for file_or_folder in os.listdir(path):
        if file_or_folder == filename:
            return True
    return False

def load_all_items():
    with open(os.getcwd() + '\\all_items_dictionary.json') as fp:
        f = json.load(fp)
    return f

def load_all_listings():
    with open(os.getcwd() + '\\all_listings_dictionary.json') as fp:
        f = json.load(fp)
    return f

def load_owned():
    with open(os.getcwd() + '\\owned_dictionary.json') as fp:
        f = json.load(fp)
    return f




""""--------------------------------------------------------------------------------------------------------------------
Load Local Files
---------------------------------------------------------------------------------------------------------------------"""

all_items_dictionary = load_all_items()

all_listings_dictionary = load_all_listings()

owned_dictionary = load_owned()

""""--------------------------------------------------------------------------------------------------------------------
Get the Item Id
---------------------------------------------------------------------------------------------------------------------"""
def get_item_id(item):
    i = all_items_dictionary[item]
    return i['id']

""""--------------------------------------------------------------------------------------------------------------------
Get the Item Name
---------------------------------------------------------------------------------------------------------------------"""
def get_item_name(item):
    i = all_items_dictionary[item]
    return i['name']

""""--------------------------------------------------------------------------------------------------------------------
Search Owned Items for Item
---------------------------------------------------------------------------------------------------------------------"""
def search_owned(id):
    if id in owned_dictionary:
        print(owned_dictionary[id])


""""--------------------------------------------------------------------------------------------------------------------
Search Prompt
---------------------------------------------------------------------------------------------------------------------"""

def run():
    input = raw_input("Please enter an item name or id: ")

    if input in all_items_dictionary:
        item = all_items_dictionary[input]
        id = str(item['id'])
        search_owned(id)

    run()
run()






