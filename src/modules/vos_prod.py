import modules.bdd as bdd
from flask import Flask , render_template , request , redirect , g , url_for,flash
from flask import session

def prod_parti():
    id = 0
    nom=session['connexion']['pseudo']
    query='''SELECT id from User WHERE pseudo = ?'''
    arg=[nom,]
    cursor=bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id=cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car 
    query2='''SELECT Produit.typeProduit,Produit.prix,Produit.description, ImageProduit.path, horaires.dateHeures, horaires.debut, horaires.fin, produit.name, produit.quantite FROM Produit join ProduitUser on Produit.id=ProduitUser.idProduit 
    join ImageProduit on ImageProduit.idProduit = Produit.id join horaires on horaires.idHeure = Produit.idHeure 
    WHERE ProduitUser.idUser=? and Produit.valid = "ok"'''
    arg2=[id]
    cursor2=bdd.get_db().cursor()
    cursor2.execute(query2,arg2)
    data=cursor2.fetchall()
    return data

def prod_jardin():
    id = 0
    id_jardin=0
    nom=session['connexion']['pseudo']
    query='''SELECT id from User WHERE pseudo = ?'''
    arg=[nom,]
    cursor=bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id=cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car 
    query2='''SELECT JardinPartage.id from JardinPartage join User on User.id = JardinPartage.ownerId WHERE JardinPartage.ownerId=?'''
    arg2=[id]
    cursor2=bdd.get_db().cursor()
    cursor2.execute(query2,arg2)
    string_id_jardin=cursor2.fetchall()[0]
    for car in string_id_jardin:
        if car not in ["(",")",","]:
            id_jardin = car 
    query3 = '''SELECT Produit.typeProduit,Produit.prix,Produit.description, ImageProduit.path, horaires.dateHeures, horaires.debut, horaires.fin,produit.name, produit.quantite FROM Produit 
    join produitjardinspartages on Produit.id = produitjardinspartages.idProduit join jardinpartage on jardinpartage.id = produitjardinspartages.idJardin
    join ImageProduit on ImageProduit.idProduit = Produit.id join horaires on horaires.idHeure = produit.idHeure 
    WHERE produitjardinspartages.idJardin = ? and Produit.valid = "ok" '''
    arg3=[id_jardin]
    cursor3=bdd.get_db().cursor()
    cursor3.execute(query3,arg3)
    data=cursor3.fetchall()
    return data

def prod_micro():
    id = 0
    id_micro=0
    nom=session['connexion']['pseudo']
    query='''SELECT id from User WHERE pseudo = ?'''
    arg=[nom,]
    cursor=bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id=cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car 
    query2='''SELECT MicroFerme.id from MicroFerme join User on User.id = MicroFerme.ownerId WHERE MicroFerme.ownerId=?'''
    arg2=[id]
    cursor2=bdd.get_db().cursor()
    cursor2.execute(query2,arg2)
    string_id_micro=cursor2.fetchall()[0]
    for car in string_id_micro:
        if car not in ["(",")",","]:
            id_micro = car 
    query3 = '''SELECT Produit.typeProduit,Produit.prix,Produit.description, ImageProduit.path, horaires.dateHeures, horaires.debut, horaires.fin, produit.name, produit.quantite FROM Produit 
    join ProduitMicroFerme on Produit.id=ProduitMicroFerme.idProduit join MicroFerme on MicroFerme.id = ProduitMicroFerme.idMicroFerme
    join ImageProduit on ImageProduit.idProduit = Produit.id join horaires on horaires.idHeure = produit.idHeure 
    WHERE ProduitMicroFerme.idMicroFerme= ? and Produit.valid = "ok"'''
    arg3=[id_micro]
    cursor3=bdd.get_db().cursor()
    cursor3.execute(query3,arg3)
    data=cursor3.fetchall()
    return data