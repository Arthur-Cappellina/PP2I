import modules.bdd as bdd
import modules.user as user
from datetime import date
from flask import session, redirect

# Méthode permettant de récupérer un produit
def get_product(id): 
    return bdd.select("Produit", conditions={"id": id})[0]

# Méthode permettant de récupérer les images d'un produit
def get_images(id): 
    images = bdd.select("ImageProduit", attributs=["path"],conditions={"idProduit": id})
    if len(images)>0:
        return images
    else: 
        return [["img/not-found.png"]]

# Méthode permettant de récupérer le vendeur du produit 
def get_owner(id):
    jardin = bdd.select("ProduitJardinsPartages", conditions={"idProduit": id})
    if len(jardin) > 0:
        return (bdd.select("JardinPartage", conditions={"id": jardin[0][1]})[0][4], 'jardin/' + str(jardin[0][1]))
    ferme = bdd.select("ProduitMicroFerme", conditions={"idProduit": id})
    if len(ferme) > 0:
        return (bdd.select("MicroFerme", conditions={"id": ferme[0][1]})[0][2], 'microferme/' + str(ferme[0][1]))
    user = bdd.select("ProduitUser", conditions={"idProduit": id})
    if len(user) > 0:
        return (bdd.select("User", conditions={"id": user[0][1]})[0][2], 'user/' + str(user[0][1]))
    return ""

# Méthode permettant d'ajouter un produit au panier 
def addToCart(request, id):
    if "panier" not in session:
        session["panier"] = {}
    session["panier"][id] = request.form['quantity']
    session.modified = True

# Méthode renvoyant les données formattés pour la page produit
def get_data_formatted(id, request): 
    if request.method=='POST' and len(request.form) > 0:
        addToCart(request, id)
    product = get_product(id)
    images = [k[0] for k in get_images(id)]
    seller = get_owner(id)
    data = {
        "id": product[0],
        "title": product[7],
        "price": product[2],
        "description": product[4],
        "quantity": product[3],
        "category": product[1],
        "vendeur": {
            "name": seller[0], 
            "link": request.url_root + seller[1]
        },
        "image": images
    }
    return data 

# Méthode utiliser lorque l'utilisateur clique sur commander 
def commander():
    id = bdd.select("user", ["id"],  {"pseudo": session["connexion"]["pseudo"]})[0][0]
    commande = bdd.select("commande")
    prix = get_price()
    cagnotte = session['connexion']['cagnotte']
    pseudo = session['connexion']['pseudo']
    latitude = session['connexion']['latitude']
    longitude = session['connexion']['longitude']
    idLocation = session['connexion']['idlocation']
    if "panier" in session and user.isConnected(): 
        if prix < cagnotte:
            for i in session["panier"]: 
                bdd.update("Produit", attribut=["quantite"], new_values=[bdd.select("Produit", conditions={"id": i})[0][3] - int(session["panier"][i])], conditions={"id": i})
                bdd.insert("Commande", valeurs=[str(len(commande)+1), i, str(id), session["panier"][i], str(date.today()), "0"])
            bdd.update('User',attribut=['cagnotte'], new_values=[cagnotte-prix], conditions={"id":id})
            cagnotte = bdd.select("user",['cagnotte'], conditions={"id":id})
            session.pop('connexion')
            session['connexion'] = {
            'pseudo': pseudo,
            'latitude': latitude,
            'longitude': longitude,
            'idlocation': idLocation,
            'cagnotte': cagnotte[0][0]
            }
    session["panier"] = {}

def get_product_cart(request): 
    if request.method=='POST':
        commander()
    elif len(request.args) > 0 and "delete" in request.args:
        del session["panier"][request.args["delete"]]
        session.modified = True
        return redirect(request.url_root + "panier")
    if "panier" in session:
        products = []
        for i in session["panier"]:
            product = get_product(i)
            data = {
                "id": product[0],
                "name": product[7],
                "price": product[2],
                "desc": product[4],
                "quantity": float(session["panier"][i]),
                "category": product[1],
                "img": get_images(i)[0][0]
            }
            products.append(data)
        price = sum([p["price"] * p["quantity"] for p in products])
        all_products = {
            "products": products,
            "total": price
        }
        return all_products
    return {}

def get_price():
    products = []
    for i in session["panier"]:
        product = get_product(i)
        data = {
            "id": product[0],
            "name": product[7],
            "price": product[2],
            "desc": product[4],
            "quantity": float(session["panier"][i]),
            "category": product[1],
            "img": get_images(i)[0][0]
        }
        products.append(data)
    price = sum([p["price"] * p["quantity"] for p in products])
    return price
    