import modules.bdd as bdd
import modules.user as user
import random
import math
from flask import session

DATABASE = "database/database.db"


def get_dernier_ajouts(): 
    amap = bdd.select("AMAP", limit=3, distinct=" DISTINCT ", order=" ORDER BY id ")
    return amap

def get_jardins():
    amap = bdd.select("jardinpartage", limit=3)
    return amap

def get_amap_correctly(amaps): 
    ajouts_json = []
    for a in amaps:
        temp_ajout = {}
        temp_ajout["img"] = a[3]
        temp_ajout["title"] = a[4]
        temp_ajout["desc"] = a[2]
        temp_ajout["type"] = "AMAP"
        temp_ajout["link"] = "/amap/" + str(a[0])
        ajouts_json.append(temp_ajout)
    return ajouts_json

def get_one_jardin(j): 
    temp_ajout = {}
    try:
        img = bdd.select("ImageJardin", ["path"], {"idJardin": j[0]}, 1)[0]
    except: 
        img = ["img/not-found.png"]
    temp_ajout["img"] = img[0]
    temp_ajout["title"] = j[4]
    temp_ajout["desc"] = j[5]
    temp_ajout["type"] = "Jardin partagé"
    temp_ajout["link"] = "/jardin-partage/" + str(j[0])
    return temp_ajout

def get_one_ferme(f): 
    temp_ajout = {}
    try:
        img = bdd.select("ImageFerme", ["path"], {"idFerme": f[0]}, 1)[0]
    except: 
        img = ["img/not-found.png"]
    temp_ajout["img"] = img[0]
    temp_ajout["title"] = f[2]
    temp_ajout["desc"] = f[1]
    temp_ajout["type"] = "Micro ferme"
    temp_ajout["link"] = "/micro-ferme/" + str(f[0])
    return temp_ajout

def get_jardins_correctly(jardins): 
    return [get_one_jardin(j) for j in jardins]

# Cette méthode retourne ce qu'il sera affiché s'il on est pas connecté
def show_for_not_connected(): 
    amaps = get_amap_correctly(get_dernier_ajouts())
    jardins = get_jardins_correctly(get_jardins())
    data = {
        'content': [
            {
                'title': 'Les nouvelles AMAP',
                'inner-content': amaps
            },
            {
                'title': 'Les derniers jardins partagés',
                'inner-content': jardins
            }
        ]
    }
    return data

# Cette méthode retourne ce qu'il sera affiché s'il on est pas connecté
def show_for_connected(): 
    amaps = get_amap_correctly(get_dernier_ajouts())
    preferences = get_preferences()
    formatted_preferences = []
    for p in preferences: 
        if len(str(p)) > 2: 
            if p[len(p) - 1] == "jardin": 
                formatted_preferences.append(get_one_jardin(p))
            elif p[len(p) - 1] == "ferme":
                formatted_preferences.append(get_one_ferme(p)) 
    data = {
        'content': [
            {
                'title': 'Cela pourrait vous plaire', 
                'inner-content': formatted_preferences
            },
            {
                'title': 'Les nouvelles AMAP',
                'inner-content': amaps
            }
        ]
    }
    return data

# Méthode permettant de proposer 3 associations / jardins / 
def get_preferences(): 
    jardins = bdd.select("jardinpartage")
    fermes = bdd.select("microferme")
    user_products = bdd.select("produit", conditions={"iduser": 1}, tables_jointes={"produituser": "id = idProduit"})
    keep_max = {1: -1, 2: -1, 3: -1}
    for f in fermes: 
        products = bdd.select("produit", conditions={"idMicroFerme": f[0]}, tables_jointes={"produitmicroferme": "id = idProduit"})
        temp_score = get_score(user_products, products) * get_localisation_factor()
        if temp_score > min(keep_max.values()): 
            del keep_max[get_key_from_value(keep_max, min(keep_max.values()))]
            f =  f + ("ferme",)
            keep_max[f] = temp_score
    for j in jardins: 
        products = bdd.select("produit", conditions={"idJardin": j[0]}, tables_jointes={"produitjardinspartages": "id = idProduit"})
        temp_score = get_score(user_products, products) * get_localisation_factor()
        if temp_score > min(keep_max.values()): 
            del keep_max[get_key_from_value(keep_max, min(keep_max.values()))]
            j = j + ("jardin",)
            keep_max[j] = temp_score
    return keep_max

def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None

def get_score(user_products, products): 
    # Le but est de récupérer le pourcentage de chaque type que la ferme propose 
    # De multiplier ce pourcentage par le nombre de produit qu'à commandé l'utilisateur
    # De multiplier à nouveau par le facteur de localisation, ainsi on obtient une valeur cohérente 
    type_of_products = get_dict_type(products, 1)
    type_of_user_products = get_dict_type(user_products, 1)
    if len(user_products) != 0:
        return get_score_from_type(type_of_user_products, type_of_products, len(user_products))
    else :
        return get_score_from_type(type_of_user_products, type_of_products, 1)
def get_score_from_type(type_of_user_products, type_of_products, l):
    # On compte le nombre de produit ayant le même type 
    similar = 0
    not_similar = 1
    for t in type_of_user_products: 
        if t in type_of_products and type_of_products[t] > 0:
            type_of_products[t] -= 1
            similar += 1 
        else: 
            not_similar += 1
    return similar / l
# Méthode permettant de compter le nombre de type d'un produit
def get_dict_type(tab, index): 
    dictionary = {}
    for t in tab: 
        if dictionary.__contains__(t[index]):
            dictionary[t[1]] = dictionary[t[index]] + 1
        else: 
            dictionary[t[1]] = 1
    return dictionary

# Méthode renvoyant un facteur de localisation entre 2 adresses
def get_localisation_factor(lat1=48.3821, long1=4.5709, lat2=48.4137, long2=5.1105): 
    distance = bdd.distance(lat1, long1, lat2, long2)
    if distance == 0: 
        return 1
    factor = 1 / distance
    return factor

def get_data():
    if user.isConnected(): 
        data = show_for_connected()
    else:
        data = show_for_not_connected()
    return data
