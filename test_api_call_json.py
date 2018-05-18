import urllib.parse
import requests

main_api = 'https://api.guildwars2.com/v2'


sub_api = '/commerce/listings'
index_number = '/19699'
url = main_api + sub_api + index_number
print(url)

json_data = requests.get(url).json()
print(json_data)
for item in json_data:
    #print(key)
    for key in item:
        #print(sub_key)
        if(key == 'name'):
            print(item[key])

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
json_dictionary_keys = {'basic' : ['id','name','type'], 'all' : ['chat_link','name','icon','description','type','rarity','level','vendor_value','default_skin','flags','game_types','restrictions','details']}

dictionary_all_items = {}

def update_dictionary_all_items():
    for item in json_data:
        item_id = str(item['id'])
        dictionary_all_items.update(item_id,item)

def get_basic():
    list_of_keys = json_dictionary_keys['basic']
    print(list_of_keys)
    for key in list_of_keys:
        print(key + ': ' + str(json_data[key]))


def get_all():
    """
    dictionary format:
    Dictionary_All_Items = {id_number : {'id': id_number, 'name': name, ect....}}
    """
    dictionary_all_items.update(json_data['id'],{'id':json_data['id']})
    list_of_keys = json_dictionary_keys['all']
    print(list_of_keys)
    for key in list_of_keys:
        print(key + ': ' + json_data[key])
        dictionary_all_items[json_data['id']].update(key,json_data['key'])

update_dictionary_all_items()

