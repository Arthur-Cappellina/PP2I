import modules.bdd as bdd
import modules.user as user

def get_all(table_name="amap", title_index=4, img_index=3, desc_index=2, icon="img/logo_associations.png", idAllowed=["all"], name=""):
    data = bdd.select(table_name, tables_jointes={"Locations": table_name + ".idLocation = locations.idLocation"})
    data_formatted = []
    for a in data: 
        temp_data = {}
        temp_data["id"] = a[0]
        temp_data["img"] = a[img_index]
        temp_data["title"] = a[title_index]
        temp_data["lat"] = a[len(a) - 2]
        temp_data["lng"] = a[len(a) - 1]
        temp_data["icon"] = icon
        temp_data["desc"] = a[desc_index]
        temp_data["link"] = name + "/" + str(a[0])
        data_formatted.append(temp_data)
    return data_formatted

def get_all_sellers():
    data = bdd.select("user", attributs=["id,pseudo,latitude,longitude"],tables_jointes={"Locations": "user.idLocation = locations.idLocation", "ProduitUser": "id = idUser"})
    users = []
    user = {}
    for d in data: 
        user["id"] = d[0]
        user["img"] = "img/user.png"
        user["title"] = d[1]
        user["lat"] = d[2]
        user["lng"] = d[3]
        user["icon"] = "img/user.png"
        user["desc"] = ""
        user["link"] = "user/" + str(d[0])
        users.append(user)
    return users

# Méthode permettant de récupérer toutes les locations correspondant au filtre donnés par l'utilisateur
# filters : {"statut": "payant", "type": ["fruits", "legumes"]""}
def get_all_locations(request):
    filters = manage_filters(request)
    data = []
    jardins = get_all("jardinpartage", icon="img/digging.png", name="jardin-partage")
    fermes = get_all("microferme", 2, icon="img/grange.png", name="micro-ferme")
    sellers = get_all_sellers()
    for f in fermes:
        try:
            img = bdd.select("ImageFerme", ["path"], {"idFerme": f["id"]}, 1)[0][0]
        except: 
            img = "img/jardin-2.jpg"
        f["img"] = img
    # L'objectif est de filtrer les jardins, fermes et utilisateurs en fonction des filtres
    if "statut" in filters:
        if len(filters["statut"]["payant"]) > 0:
            (fermes, jardins, sellers) = filter_on_prices(fermes, jardins, sellers, False)
        elif len(filters["statut"]["gratuit"]) > 0:
            (fermes, jardins, sellers) = filter_on_prices(fermes, jardins, sellers)
    if "type" in filters:
        (fermes, jardins, sellers) = filter_on_product(filters["type"], fermes, jardins, sellers)
    all_choice = len(filters["choice"]["amaps"]) == 0 and len(filters["choice"]["jardin"]) == 0 and len(filters["choice"]["ferme"]) == 0 and len(filters["choice"]["indé"]) == 0
    if len(filters["choice"]["amaps"]) > 0 or all_choice:
        data.extend(get_all())
    if len(filters["choice"]["jardin"]) > 0 or all_choice:
        data.extend(jardins)
    if len(filters["choice"]["ferme"]) > 0 or all_choice:
        data.extend(fermes)
    if len(filters["choice"]["indé"]) >  0 or all_choice:
        data.extend(sellers)
    return (data, filters)

def get_map_data(request): 
    (locations, params) = get_all_locations(request)
    pos = {'lat': 48.6936184, 'lng': 6.1832413}
    if user.isConnected():
        pos = {'lat': user.get_user_position()[0], 'lng': user.get_user_position()[1]}
    data = {
        'currentLocation': pos,
        'nearPoints': locations,
        "params": params
    }
    return data

def manage_filters(request): 
    params = {"statut": {"tous": "", "gratuit": "", "payant": ""}, "type": {}, "choice": {"amaps": "", "jardin":"", "ferme": "", "indé": ""}}
    if "statut" in request.args:
        params["statut"][request.args['statut']] = "selected"
    else: 
        params["statut"]["tous"] = "selected"
    if "type" in request.args:
        for t in request.args.getlist('type'):
            params["type"][t] = "tag-selected"
    if "choice" in request.args:
        for c in request.args.getlist('choice'):
            params["choice"][c] = "type-selected"
    types = get_all_type()
    for t in types:
        if t[0] not in params["type"]:
            params["type"][t[0]] = ""
    return params

def get_all_type(): 
    return bdd.select("Produit", ["name"], distinct="distinct", order=" order by typeProduit, name")

def general_filters(products, fermes, jardins, users, free=True):
    free_products_id = [p[0] for p in products]
    jar = []
    for j in jardins: 
        jardin_product = bdd.select("ProduitJardinsPartages", tables_jointes={"JardinPartage": "idJardin = id"}, conditions={"idJardin": j["id"]})
        current_products = [k[0] for k in jardin_product]
        for c in current_products:
            if (c in free_products_id and free) or (c not in free_products_id and not free) and j not in jar:
                jar.append(j)
    fer = []
    for f in fermes: 
        ferme_product = bdd.select("ProduitMicroFerme", tables_jointes={"MicroFerme": "idMicroFerme = id"}, conditions={"idMicroFerme": f["id"]})
        current_products = [k[0] for k in ferme_product]
        for c in current_products:
            if (c in free_products_id and free) or (c not in free_products_id and not free) and f not in fer:
                fer.append(f)
    us = []
    for u in users: 
        ferme_product = bdd.select("ProduitUser", tables_jointes={"User": "idUser = id"}, conditions={"idUser": u["id"]})
        current_products = [k[0] for k in ferme_product]
        for c in current_products:
            if (c in free_products_id and free) or (c not in free_products_id and not free) and u not in us:
                us.append(u)
    return (fer, jar, us)

def filter_on_prices(fermes, jardins, users, free=True):
    free_products = bdd.select("produit", conditions={"prix": 0})
    return general_filters(free_products, fermes, jardins, users, free)

def filter_on_product(products, fermes, jardins, users, free=True):
    allowed = [k for k in products if len(products[k]) > 0]
    if len(allowed) == 0:
        return (fermes, jardins, users)
    products_allowed = []
    conditions = {}
    for c in allowed:
        conditions["name"] = c
        products_allowed.append([bdd.select("produit", conditions=conditions)[0][0]])
    return general_filters(products_allowed, fermes, jardins, users, free)