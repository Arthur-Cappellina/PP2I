import modules.bdd as bdd

def get_element(id, table, cond_table):
    return bdd.select(table, conditions={cond_table: id})[0]

def get_element_image(id, table, cond_table):
    try:
        return bdd.select("imageferme", conditions={"idFerme": id})[0][2]
    except:
        return "img/not-found.png"

def get_adresse(idLocation):     
    try:
        return bdd.select("locations", conditions={"idLocation": idLocation})[0][1]
    except:
        return "Adresse non communiquée"

def get_produits(id, table, conditions): 
    produits_ids = bdd.select(table, conditions={conditions: id})
    produits = []
    for p in produits_ids:
        current_produit = bdd.select("produit", conditions={"id": p[0]})[0]
        if current_produit[9] == "ok":
            produits.append(bdd.select("produit", conditions={"id": p[0]}))
    return produits

def get_produits_image(idProduit):
    try: 
        return bdd.select("imageproduit", conditions={"idProduit": idProduit})[0][2]
    except: 
        return "img/not-found.png"

def format_product(produit):
    data = {
        "id": produit[0],
        "title": produit[7],
        "type": produit[1],
        "quantite": produit[3],
        "prix": produit[2],
        "image": get_produits_image(produit[0])
    }
    return data

def get_data(id):
    ferme = get_element(id, "microferme", "id")
    images = get_element_image(id, "imageferme", "idFerme")
    produits = get_produits(id, "produitmicroferme", "idMicroFerme")
    return format_data(ferme[2], ferme[1], images, "Microferme", 4, produits)

def format_data(title, desc, image, type, idLocation, produits): 
    adresse = get_adresse(idLocation)
    produits_formatted = []
    for i in range(len(produits)):
        produits_formatted.append(format_product(produits[i][0])) 
    data = {
        "type": type,
        "title": title,
        "adresse": adresse,
        "image": image,
        "description": desc,
        "produits": produits_formatted
    }
    return data

def get_data_jardin(id):
    jardin = get_element(id, "jardinpartage", "id")
    images = get_element_image(id, "imagejardinpartage", "idJardinPartage")
    produits = get_produits(id, "produitjardinspartages", "idJardin")
    return format_data(jardin[4], jardin[6], images, "Jardin partagé", 3, produits)

def get_data_user(id):
    user = get_element(id, "user", "id")
    images = user[5]
    produits = get_produits(id, "produituser", "idUser")
    return format_data(user[2], user[1], images, "Vendeur indépendendant", user[8], produits)