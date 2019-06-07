import urllib.parse
import requests
import datetime
import os
import json

main_api = 'https://api.guildwars2.com/v2'

sub_api = '/commerce/listings'
# index_number = '/19699'
url = main_api + sub_api
## + index_number
print(url)

sub_bank_api = '/account/bank'
sub_materials_api = '/account/materials'
authorization = {'Authorization': 'Bearer '}

bank_url = main_api + sub_bank_api
materials_url = main_api + sub_materials_api

number_list = requests.get(url).json()
json_bank_data = requests.get(bank_url, headers=authorization).json()
json_materials_data = requests.get(materials_url, headers=authorization).json()
# print(json_bank_data)
# for item in json_bank_data:
#    if(item == None):
#        print("Empty Box")
#    else:
#        for key in item:
#            #print(sub_key)
#            if(key == 'id'):
#                print(item[key])
#            if(key == 'count'):
#                print(item[key])


""" Dictionary keys in Items Json request:
'id'            (number) = Item id
'chat_link'     (string) = chat link
'name'          (string) = name of item
'icon'          (string) = Full icon URL
'description'   (string) = The item description
'type'          (string) = Armor, Back (Back Item), Bag, Consumable, Container, CraftingMaterial (Crafting Materials), 
                           Gathering, Gizmo, MiniPet (Miniatures), Tool (Salvage Kits), Trait (Trait Guides), Trinket, 
                           Trophy, UpgradeComponent, Weapon
'rarity'        (string) = Junk, Basic, Fine, Masterwork, Rare, Exotic, Ascended, Legendary
'level'         (number) = The required level
'vendor_value'  (number) = The value in coins when selling to a vendor. (Can be non-zero even if has NoSell flag
'flags'         (array of strings) = AccountBindOnUse (Account bound on use), 
                                     Account Bound (Account bound on aquire), 
                                     Attuned (Upgraded in Mystic Forge to gain additional infusion slot), 
                                     BulkConsume (if the item can be bulk consumed), 
                                     DeleteWarning (if the item will prompt the player with a warning when deleting), 
                                     Hidesuffix (hide the suffix of the upgrade component),
                                     Infused (if the item is infused,
                                     MonsterOnly,
                                     NoMysticForge (not usable in the Mystic Forge,
                                     NoSalvage (not salvageable),
                                     NoSell (not sellable),
                                     NotUpgradable (not upgradable),
                                     NoUnderwater (not available underwater),
                                     SoulbindOnAquire (soulbound on aquire),
                                     Tonic (if the item is a tonic),
                                     Unique (unique)
'game_types'    (array of strings) = Activity (usable in activities),
                                     Dungeon (usable in dungeon),
                                     Pve (Usable in general PvE),
                                     PvP (Usable in PvP),
                                     PvpLobby (Usable in Heart of the Mists
                                     WvW (Usable in World v World)
'restrictions'  (array of strings) = Asura, Charr, Human, Norn, Sylvari, Elementalist, Engineer, Guardian, Mesmer,
                                     Necromancer, Ranger, Theif, Warrior
'details'       (object, optional) = Additional item details if applicable, depending on the type of the item
"""

dictionary_all_items = dict()

dictionary_bank = dict()

dictionary_materials = dict()

item = 0

def file_exists(path, filename):
    for file_or_folder in os.listdir(path):
        if file_or_folder == filename:
            return True
    return False

def has_expired(date):
    date = date.split('-',3)
    return (datetime.date.today() - datetime.date(int(date[0]), int(date[1]), int(date[2]))) > datetime.timedelta(7)

def save_bank(dict):
    with open('bank_dictionary.json', 'w') as outfile:
        json.dump(dict, outfile)
#    f = open('bank_dictionary.txt', 'w')
#    f.write(str(dict))
#    f.close()


def load_bank():
    with open(os.getcwd() + '\\bank_dictionary.json') as fp:
        f = json.load(fp)
    return f
#    f = open('bank_dictionary.txt', 'r')
#    data = f.read()
#    f.close()
#   return eval(data)


def save_mats(dict):
    with open('mats_dictionary.json', 'w') as outfile:
        json.dump(dict, outfile)
#    f = open('mats_dictionary.txt', 'w')
#    f.write(str(dict))
#    f.close()


def load_mats():
    with open(os.getcwd() + '\\mats_dictionary.json') as fp:
        f = json.load(fp)
    return f
#    f = open('mats_dictionary.txt', 'r')
#    data = f.read()
#    f.close()
#    return eval(data)


def save_all_items(dict):
     with open('all_items_dictionary.json','w') as outfile:
         json.dump(dict, outfile)
#    f = open('all_items_dictionary.txt', 'w')
#    f.write(str(dict))
#    f.close()


def load_all_items():
    with open(os.getcwd() + '\\all_items_dictionary.json') as fp:
        f = json.load(fp)
    return f
    #f = json.load(fp)

#    f = open('all_items_dictionary.txt', 'r')
#    data = f.read()
#    f.close()
#    return eval(data)


def segment_number_list(number_list):
    list = []
    string = ""
    list_len = len(number_list)
    count = 0

    for n in number_list:
        if count == 199:
            list.append(string)
            count = 0
            string = ""
        elif count == 198:
            string = string + str(n)
            count = count + 1
        else:
            string = string + str(n) + ','
            count = count + 1
    return list


def acquire_listings(number_list):

    result = dict()


    if file_exists(os.getcwd(), 'all_items_dictionary.json') == True:
        saved_dict = load_all_items()
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})

        if has_expired(saved_dict['date']):
            number_list = segment_number_list(number_list)
            for n in number_list:
                temp_url = main_api + sub_api + '?ids=' + str(n)
                listings = requests.get(temp_url).json()
                for l in listings:
                    id = l['id']
                    buys = l['buys']
                    sells = l['sells']
                    result.update({id: {'buys': buys, 'sells': sells}})
                    print(str(id))

            return result
        return saved_dict
    else:
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
        number_list = segment_number_list(number_list)
        for n in number_list:
            temp_url = main_api + sub_api + '?ids=' + str(n)
            listings = requests.get(temp_url).json()
            for l in listings:
                id = l['id']
                buys = l['buys']
                sells = l['sells']
                result.update({id: {'buys': buys, 'sells': sells}})
                print(str(id))

        return result


def update_dictionary_all_items(number_list):
    ##   json_data = requests.get(url).json()
    ##    for item in json_data:
    ##        if item != None or item != list:
    ##            item_id = json_data[item]
    ##            u = {item_id: item}
    ##            dictionary_all_items.update(u)
    ##    save_all_items(dictionary_all_items) */
    return acquire_listings(number_list)


def get_basic():
    list_of_keys = json_dictionary_keys['basic']
    print(list_of_keys)
    for key in list_of_keys:
        print(key + ': ' + str(json_data[key]))


def update_bank():
    result = dict()


    if file_exists(os.getcwd(), 'bank_dictionary.json') == True:
        saved_dict = load_bank()
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})

        if has_expired(saved_dict['date']):
            for item in json_bank_data:
                if (item != None):
                    item_id = str(item['id'])
                    result.update({item_id: item})
        #    save_bank(dictionary_bank)
            return result
        return saved_dict
    else:
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
        for item in json_bank_data:
           if (item != None):
               item_id = str(item['id'])
               result.update({item_id: item})
        #   save_bank(dictionary_bank)
        return result



def update_material_storage():


    result = dict()

    if file_exists(os.getcwd(), 'mats_dictionary.json') == True:
        saved_dict = load_mats()
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})

        if has_expired(saved_dict['date']):
            for item in json_materials_data:
                if (item != None):
                    item_id = str(item['id'])
                    result.update({item_id: item})
        #    save_mats(dictionary_materials)
            return result
        return saved_dict
    else:
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})

        for item in json_materials_data:
           if (item != None):
               item_id = str(item['id'])
               result.update({item_id: item})
   #    save_mats(dictionary_materials)
        return result


#def get_all():
#    """
#    dictionary format:
#    Dictionary_All_Items = {id_number : {'id': id_number, 'name': name, ect....}}
#    """
#    dictionary_all_items.update(json_data['id'], {'id': json_data['id']})
#    list_of_keys = json_dictionary_keys['all']
#    print(list_of_keys)
#    for key in list_of_keys:
#        ##print(key + ': ' + json_data[key])
#        dictionary_all_items[json_data['id']].update(key, json_data['key'])

def save_all(all_items, bank, mats):
    save_all_items(all_items)
    print("All items dictionary saved")
    save_bank(bank)
    print("Bank dictionary saved")
    save_mats(mats)
    print("Mats dictionary saved")

def update_all(dictionary_all_items, dictionary_bank, dictionary_materials):
    dictionary_all_items = update_dictionary_all_items(number_list)
    dictionary_bank = update_bank()
    dictionary_materials = update_material_storage()
    save_all(dictionary_all_items, dictionary_bank, dictionary_materials)



json_dictionary_keys = {'basic': ['id', 'name', 'type'],
                        'all': ['chat_link', 'name', 'icon', 'description', 'type', 'rarity', 'level', 'vendor_value',
                                'default_skin', 'flags', 'game_types', 'restrictions', 'details']}

update_all(dictionary_all_items, dictionary_bank, dictionary_materials)

#d = { 'date': datetime.date.today().strftime("%Y-%m-%d")}
#save_all_items(d)

#d = load_all_items()

#split = d['date'].split('-',3)
#print(datetime.date(2019, 0o6, 15) - datetime.date(int(split[0]),int(split[1]),int(split[2])))
