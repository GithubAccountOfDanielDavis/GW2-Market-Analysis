
import requests
import datetime
import os
import json

main_api = 'https://api.guildwars2.com/v2'

sub_api = '/commerce/listings'
url = main_api + sub_api
print(url)

sub_bank_api = '/account/bank'
sub_materials_api = '/account/materials'
authorization = {'Authorization': 'Bearer  """Enter API key here"""'}

check_save_all = False
check_save_all_listings = False
check_save_bank = False
check_save_mats = False
check_save_toons = False
check_save_owned = False



number_list = requests.get(url).json()


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

""""--------------------------------------------------------------------------------------------------------------------
 Check Functions
---------------------------------------------------------------------------------------------------------------------"""

def file_exists(path, filename):
    for file_or_folder in os.listdir(path):
        if file_or_folder == filename:
            return True
    return False

def has_expired(date):
    date = date.split('-',3)
    return (datetime.date.today() - datetime.date(int(date[0]), int(date[1]), int(date[2]))) > datetime.timedelta(7)



""""--------------------------------------------------------------------------------------------------------------------
Initialize Values
---------------------------------------------------------------------------------------------------------------------"""


dictionary_all_items = dict()

dictionary_all_listings = dict()

dictionary_bank = dict()

dictionary_materials = dict()

dictionary_toon_list = dict()

dictionary_currency = dict()

dictionary_owned = dict()

item = 0


""""--------------------------------------------------------------------------------------------------------------------
 All Items
---------------------------------------------------------------------------------------------------------------------"""

def save_all_items(dict):
#    global check_save_all
    if check_save_all:
        with open('all_items_dictionary.json','w') as outfile:
            json.dump(dict, outfile)



def load_all_items():
    with open(os.getcwd() + '\\all_items_dictionary.json') as fp:
        f = json.load(fp)
    return f


def segment_number_list(number_list):
    list = []
    string = ""
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


def update_dictionary_all_items():
    global check_save_all
    result = dict()

    if file_exists(os.getcwd(), 'all_items_dictionary.json') == True:
        saved_dict = load_all_items()

        if has_expired(saved_dict['date']):
            result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
            all_url = main_api + '/items'
            number_list = requests.get(all_url, headers=authorization).json()

            check_save_all = True
            number_list = segment_number_list(number_list)
            for n in number_list:
                try:
                    temp_url = main_api + '/items' + '?ids=' + str(n)
                    listings = requests.get(temp_url).json()
                except:
                    print("Error in retrieving listing")

                try:
                    for l in listings:
                        """
                        id = l['id']
                        name = l['name']
                        icon = l['icon']
                        description = l['description']
                        type = l['type']
                        rarity = l['rarity']
                        level = l['level']
                        vendor_value = l['vendor_value']
                       # default_skin = l['default_skin']
                        flags = l['flags']
                        game_types = l['game_types']
                        restrictions = l['restrictions']
                        details = l['details']
                        result.update({id: {'name': name, 'icon': icon, 'description': description, 'type': type,
                                            'rarity': rarity, 'level': level, 'vendor_value': vendor_value,
                                            'default_skin': default_skin, 'flags': flags, 'game_types': game_types,
                                            'restrictions': restrictions, 'details': details}})"""
                        id = l['id']
                        name = l['name']

                        # allows for a search using Id or Name
                        result.update({name: l})
                        result.update({id: l})
                        print('item: ' + str(id))
                except:
                    print("Error in saving listing")
            return result
        return saved_dict
    else:
        all_url = main_api + '/items'
        number_list = requests.get(all_url, headers=authorization).json()

        check_save_all = True
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
        number_list = segment_number_list(number_list)

        for n in number_list:
            try:
                temp_url = main_api + '/items' + '?ids=' + str(n)
                listings = requests.get(temp_url).json()
            except:
                print("Error in retrieving listing")

            try:
                for l in listings:
                    """
                    id = l['id']
                    name = l['name']
                    icon = l['icon']
                    description = l['description']
                    type = l['type']
                    rarity = l['rarity']
                    level = l['level']
                    vendor_value = l['vendor_value']
                   # default_skin = l['default_skin']
                    flags = l['flags']
                    game_types = l['game_types']
                    restrictions = l['restrictions']
                    details = l['details']
                    result.update({id: {'name': name, 'icon': icon, 'description': description, 'type': type,
                                        'rarity': rarity, 'level': level, 'vendor_value': vendor_value,
                                        'default_skin': default_skin, 'flags': flags, 'game_types': game_types,
                                        'restrictions': restrictions, 'details': details}})"""
                    id = l['id']
                    name = l['name']

                    #allows for a search using Id or Name
                    result.update({name: l })
                    result.update({id: l})
                    print('item: ' + str(id))
            except:
                print("Error in saving listing")
        return result




""""--------------------------------------------------------------------------------------------------------------------
 Currency
---------------------------------------------------------------------------------------------------------------------"""




""""--------------------------------------------------------------------------------------------------------------------
Currency: Wallet
---------------------------------------------------------------------------------------------------------------------"""



""""--------------------------------------------------------------------------------------------------------------------
Currency: Type List
---------------------------------------------------------------------------------------------------------------------"""




""""--------------------------------------------------------------------------------------------------------------------
 Toons
---------------------------------------------------------------------------------------------------------------------"""

""""--------------------------------------------------------------------------------------------------------------------
Toons: Toon Information
---------------------------------------------------------------------------------------------------------------------"""


def get_toon_information(id):
    toon_info_url = main_api + '/characters' + '/' + id
    json_toon_info = requests.get(toon_info_url, headers=authorization).json()
    return json_toon_info


""""--------------------------------------------------------------------------------------------------------------------
Toons Toon List
---------------------------------------------------------------------------------------------------------------------"""

def save_toon_list(dict):
  #  global check_save_toons
    if check_save_toons:
        with open('toon_list_dictionary.json', 'w') as outfile:
            json.dump(dict, outfile)


def load_toon_list():
    with open(os.getcwd() + '\\toon_list_dictionary.json') as fp:
        f = json.load(fp)
    return f

def update_dictionary_toon_list():
    global check_save_toons
    toon_url = main_api + '/characters'
    json_toon_list = requests.get(toon_url, headers=authorization).json()
    result = dict()

    if file_exists(os.getcwd(), 'toon_list_dictionary.json') == True:
        saved_dict = load_toon_list()

        if has_expired(saved_dict['date']):
            result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
            check_save_toons = True
            count = 0
            for item in json_toon_list:
                if (item != None):
                    item_id = str(item)
                    result.update({item_id: get_toon_information(item_id)})
                    count = count + 1
            return result
        return saved_dict
    else:
        check_save_toons = True
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
        for item in json_toon_list:
            count = 0
            if (item != None):
                item_id = str(item)
                result.update({item_id: get_toon_information(item_id)})
                count = count + 1
        return result



""""--------------------------------------------------------------------------------------------------------------------
 All Listings
---------------------------------------------------------------------------------------------------------------------"""

def save_all_listings(dict):
#    global check_save_all
    if check_save_all_listings:
        with open('all_listings_dictionary.json','w') as outfile:
            json.dump(dict, outfile)



def load_all_listings():
    with open(os.getcwd() + '\\all_listings_dictionary.json') as fp:
        f = json.load(fp)
    return f


def segment_number_list(number_list):
    list = []
    string = ""
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


def update_dictionary_all_listings(number_list):
    global check_save_all_listings
    result = dict()

    if file_exists(os.getcwd(), 'all_listings_dictionary.json') == True:
        saved_dict = load_all_listings()

        if has_expired(saved_dict['date']):
            result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
            check_save_all_listings = True
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
        check_save_all_listings = True
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
        number_list = segment_number_list(number_list)
        for n in number_list:
            try:
                temp_url = main_api + sub_api + '?ids=' + str(n)
                listings = requests.get(temp_url).json()

                for l in listings:
                    id = l['id']
                    buys = l['buys']
                    sells = l['sells']
                    result.update({id: {'buys': buys, 'sells': sells}})
                    print(str(id))
            except:
                print("Error in retrieving listing")
        return result


""""--------------------------------------------------------------------------------------------------------------------
 Account Bank
---------------------------------------------------------------------------------------------------------------------"""


def save_bank(dict):
 #   global check_save_bank
    if check_save_bank:
        with open('bank_dictionary.json', 'w') as outfile:
            json.dump(dict, outfile)


def load_bank():
    with open(os.getcwd() + '\\bank_dictionary.json') as fp:
        f = json.load(fp)
    return f


def update_bank():
    global check_save_bank
    bank_url = main_api + sub_bank_api
    json_bank_data = requests.get(bank_url, headers=authorization).json()
    result = dict()

    if file_exists(os.getcwd(), 'bank_dictionary.json') == True:
        saved_dict = load_bank()


        if has_expired(saved_dict['date']):
            result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
            check_save_bank = True
            for item in json_bank_data:
                if (item != None):
                    item_id = str(item['id'])
                    result.update({item_id: item})
        #    save_bank(dictionary_bank)
            return result
        return saved_dict
    else:
        check_save_bank = True
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
        for item in json_bank_data:
           if (item != None):
               item_id = str(item['id'])
               result.update({item_id: item})
        return result

""""--------------------------------------------------------------------------------------------------------------------
Material Storage
---------------------------------------------------------------------------------------------------------------------"""

def save_mats(dict):
  #  global check_save_mats
    if check_save_mats:
        with open('mats_dictionary.json', 'w') as outfile:
            json.dump(dict, outfile)


def load_mats():
    with open(os.getcwd() + '\\mats_dictionary.json') as fp:
        f = json.load(fp)
    return f



def update_material_storage():
    global check_save_mats
    materials_url = main_api + sub_materials_api
    json_materials_data = requests.get(materials_url, headers=authorization).json()
    result = dict()

    if file_exists(os.getcwd(), 'mats_dictionary.json') == True:
        saved_dict = load_mats()


        if has_expired(saved_dict['date']):
            result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})
            check_save_mats = True
            for item in json_materials_data:
                if (item != None):
                    item_id = str(item['id'])
                    result.update({item_id: item})
        #    save_mats(dictionary_materials)
            return result
        return saved_dict
    else:
        check_save_mats = True
        result.update({'date': datetime.date.today().strftime("%Y-%m-%d")})

        for item in json_materials_data:
           if (item != None):
               item_id = str(item['id'])
               result.update({item_id: item})
        return result


""""--------------------------------------------------------------------------------------------------------------------
 Owned Items
---------------------------------------------------------------------------------------------------------------------"""

def save_owned(dict):
  #  global check_save_mats
    if check_save_owned:
        with open('owned_dictionary.json', 'w') as outfile:
            json.dump(dict, outfile)


def load_owned():
    with open(os.getcwd() + '\\owned_dictionary.json') as fp:
        f = json.load(fp)
    return f

def update_owned():
    global check_save_owned
    bank = update_bank()
    mats = update_material_storage()
    toons = update_dictionary_toon_list()
    list = []
    result = dict()

    check_save_owned = True
    """ Compile list of all items """
    for b in bank:
        if (b != 'date'):
            if b not in list:
                list.append(b)
    for m in mats:
        if (m != 'date'):
            if m not in list:
                list.append(m)
    for t in toons:
        if (t != 'date'):
            for c in toons[t]:
                if c == 'bags':
                    a = toons[t]
                    b = a[c]
                    for d in b:
                        e = d['inventory']
                        for f in e:
                            if f != None:
                                g = str(f['id'])
                                if g not in list:
                                    list.append(g)

    for n in list:
        result.update({n: {'total': 0, 'bank': 0, 'mats': 0, 'Enbrimir': 0, 'All The Way Down': 0, 'Foundit All': 0,
                           'Foundit': 0, 'From On High': 0, 'Founditfirst': 0}})

    for b in bank:
        if (b != 'date'):
            c = bank[b]
            r = result[b]
            if r['bank'] > 0:
                r['bank'] = r['bank'] + c['count']
            else:
                r['bank'] = c['count']
    for m in mats:
        if (m != 'date'):
            c = mats[m]
            r = result[m]
            if r['mats'] > 0:
                r['mats'] = r['mats'] + c['count']
            else:
                r['mats'] = c['count']
    for t in toons:
        if (t != 'date'):
            for c in toons[t]:
                if c == 'bags':
                    a = toons[t]
                    b = a[c]
                    for d in b:
                        e = d['inventory']
                        for f in e:
                            if f != None:
                                g = str(f['id'])
                                r = result[g]
                                if r[t] > 0:
                                    r[t] = r[t] + f['count']
                                else:
                                    r[t] = f['count']


    for n in result:
        r = result[n]
        b = r['bank']
        m = r['mats']
        e = r['Enbrimir']
        atwd = r['All The Way Down']
        fa = r['Foundit All']
        f = r['Foundit']
        foh = r['From On High']
        ff = r['Founditfirst']
        r['total'] = b + m + e + atwd + fa + f + foh + ff

    return result

""""--------------------------------------------------------------------------------------------------------------------
Save and Update
---------------------------------------------------------------------------------------------------------------------"""


def save_all(all_items, all_listings, bank, mats, toons, owned):
 #   save_all_items(all_items)
    print("All items dictionary saved")
 #   save_all_listings(all_listings)
    print("All listings dictionary saved")
    save_bank(bank)
    print("Bank dictionary saved")
    save_mats(mats)
    print("Mats dictionary saved")
    save_toon_list(toons)
    print("Toon list saved")
    save_owned(owned)
    print("Owned dictionary saved")


def update_all(dictionary_all_items, dictionary_all_listings, dictionary_bank, dictionary_materials, dictionary_toon_list, dictionary_owned):
 #   dictionary_all_items = update_dictionary_all_items()
 #   dictionary_all_listings = update_dictionary_all_listings(number_list)
    dictionary_bank = update_bank()
    dictionary_materials = update_material_storage()
    dictionary_toon_list = update_dictionary_toon_list()
    dictionary_owned = update_owned()
    save_all(dictionary_all_items, dictionary_all_listings, dictionary_bank, dictionary_materials, dictionary_toon_list, dictionary_owned)



json_dictionary_keys = {'basic': ['id', 'name', 'type'],
                        'all': ['chat_link', 'name', 'icon', 'description', 'type', 'rarity', 'level', 'vendor_value',
                                'default_skin', 'flags', 'game_types', 'restrictions', 'details']}

update_all(dictionary_all_items, dictionary_all_listings, dictionary_bank, dictionary_materials, dictionary_toon_list, dictionary_owned)

