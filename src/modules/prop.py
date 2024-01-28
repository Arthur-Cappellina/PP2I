from flask import Flask , render_template , request , redirect , g , url_for,flash
import modules.bdd as bdd

def propo_part(date_collecte,debut_collecte,fin_collecte,name,choice,price,description,nom_prod,quantite,nom_fichier):
    id = 0
    id_prod = 0
    id_horaire = 0
    query_horaire='''INSERT INTO horaires (dateHeures,debut,fin) VALUES (?,?,?)'''
    arg_horaire = [date_collecte,debut_collecte,fin_collecte]
    db = bdd.get_db()
    cursor_horaire = db.cursor()
    cursor_horaire.execute(query_horaire,arg_horaire)
    db.commit()
    query_id_horaire='''SELECT MAX(idHeure) FROM horaires'''
    cursor_id = bdd.get_db().cursor()
    cursor_id.execute(query_id_horaire)
    string_id_horaire = cursor_id.fetchall()[0]
    for car in string_id_horaire:
        if car not in ["(",")",","]:
            id_horaire = car 
    query='''SELECT id from User WHERE pseudo = ?'''
    arg=[name,]
    cursor=bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id=cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car 
    query2 = '''INSERT INTO produit (typeProduit,prix,description,idHeure,name,quantite) VALUES (?,?,?,?,?,?)'''
    args2=[choice,price,description,id_horaire, nom_prod,quantite]
    cursor2=db.cursor()
    cursor2.execute(query2,args2)
    db.commit()
    query3='''SELECT MAX(id) FROM produit'''
    cursor3=bdd.get_db().cursor()
    cursor3.execute(query3)
    string_id_prod = cursor3.fetchall()[0]
    for car in string_id_prod:
        if car not in ["(",")",","]:
            id_prod = car 
    query4 = '''INSERT INTO produituser ( idProduit, idUser) VALUES (?, ?)'''
    args4=[id_prod,id,]
    cursor4=db.cursor()
    cursor4.execute(query4,args4)
    db.commit()
    path = "img/"+str(nom_fichier)
    query5='''INSERT INTO imageproduit (idProduit,Path) VALUES (?,?)'''
    args5=[id_prod,path]
    cursor5=db.cursor()
    cursor5.execute(query5,args5)
    db.commit()
    
def propo_micro(date_collecte,debut_collecte,fin_collecte,name,choice,price,description,nom_prod,quantite,nom_fichier):
    id = 0
    id_prod = 0
    name_mf = ''
    id_mf = 0
    id_horaire = 0
    query_horaire='''INSERT INTO horaires (dateHeures,debut,fin) VALUES (?,?,?)'''
    arg_horaire = [date_collecte,debut_collecte,fin_collecte]
    db = bdd.get_db()
    cursor_horaire = db.cursor()
    cursor_horaire.execute(query_horaire,arg_horaire)
    db.commit()
    query_id_horaire='''SELECT MAX(idHeure) FROM horaires'''
    cursor_id = bdd.get_db().cursor()
    cursor_id.execute(query_id_horaire)
    string_id_horaire = cursor_id.fetchall()[0]
    for car in string_id_horaire:
        if car not in ["(",")",","]:
            id_horaire = car 
    query='''SELECT id from User WHERE pseudo = ?'''
    arg=[name,]
    cursor=bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id=cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car
    query_int='''SELECT nom FROM MicroFerme WHERE ownerId = ?'''
    arg_int = [id,]
    cursor_int = bdd.get_db().cursor()
    cursor_int.execute(query_int,arg_int)
    string_name_mf = cursor_int.fetchall()[0]
    for car in string_name_mf:
        if car not in ["(",")",","]:
            name_mf= name_mf + car
    query2 = '''INSERT INTO produit (typeProduit,prix,description,idHeure,name,quantite) VALUES (?,?,?,?,?,?)'''
    args2=[choice,price,description,id_horaire,nom_prod,quantite]
    db = bdd.get_db()
    cursor2=db.cursor()
    cursor2.execute(query2,args2)
    db.commit()
    query3='''SELECT MAX(id) FROM produit'''
    cursor3=bdd.get_db().cursor()
    cursor3.execute(query3)
    string_id_prod = cursor3.fetchall()[0]
    for car in string_id_prod:
        if car not in ["(",")",","]:
            id_prod = car
    query_int2='''SELECT id FROM MicroFerme WHERE ownerId = ?'''
    arg_int2=[id,]
    cursor_int2 = bdd.get_db().cursor()
    cursor_int2.execute(query_int2,arg_int2)
    string_id_mf = cursor_int2.fetchall()[0]
    for car in string_id_mf:
        if car not in ["(",")",","]:
            id_mf = car
    query4 = '''INSERT INTO produitmicroferme ( idProduit, idMicroFerme) VALUES (?, ?)'''
    args4=[id_prod,id_mf,]
    cursor4=db.cursor()
    cursor4.execute(query4,args4)
    db.commit()
    path = "img/"+str(nom_fichier)
    query5='''INSERT INTO imageproduit (idProduit,Path) VALUES (?,?)'''
    args5=[id_prod,path]
    cursor5=db.cursor()
    cursor5.execute(query5,args5)
    db.commit()
    
def propo_jardin(date_collecte,debut_collecte,fin_collecte,name,choice,price,description,nom_prod,quantite,nom_fichier):
    id = 0
    id_prod = 0
    name_jp = ''
    id_jp = 0
    id_horaire = 0
    query_horaire='''INSERT INTO horaires (dateHeures,debut,fin) VALUES (?,?,?)'''
    arg_horaire = [date_collecte,debut_collecte,fin_collecte]
    db = bdd.get_db()
    cursor_horaire = db.cursor()
    cursor_horaire.execute(query_horaire,arg_horaire)
    db.commit()
    query_id_horaire='''SELECT MAX(idHeure) FROM horaires'''
    cursor_id = bdd.get_db().cursor()
    cursor_id.execute(query_id_horaire)
    string_id_horaire = cursor_id.fetchall()[0]
    for car in string_id_horaire:
        if car not in ["(",")",","]:
            id_horaire = car 
    query='''SELECT id from User WHERE pseudo = ?'''
    arg=[name,]
    cursor=bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id=cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car
    query_int='''SELECT name FROM JardinPartage WHERE ownerId = ?'''
    arg_int = [id,]
    cursor_int = bdd.get_db().cursor()
    cursor_int.execute(query_int,arg_int)
    string_name_jp = cursor_int.fetchall()[0]
    for car in string_name_jp:
        if car not in ["(",")",","]:
            name_jp= name_jp + car
    query2 = '''INSERT INTO produit (typeProduit,prix,description,idHeure,name,quantite) VALUES (?,?,?,?,?,?)'''
    args2=[choice,price,description,id_horaire,nom_prod,quantite]
    db = bdd.get_db()
    cursor2=db.cursor()
    cursor2.execute(query2,args2)
    db.commit()
    query3='''SELECT MAX(id) FROM produit'''
    cursor3=bdd.get_db().cursor()
    cursor3.execute(query3)
    string_id_prod = cursor3.fetchall()[0]
    for car in string_id_prod:
        if car not in ["(",")",","]:
            id_prod = car
    query_int2='''SELECT id FROM JardinPartage WHERE ownerId = ?'''
    arg_int2=[id,]
    cursor_int2 = bdd.get_db().cursor()
    cursor_int2.execute(query_int2,arg_int2)
    string_id_jp = cursor_int2.fetchall()[0]
    for car in string_id_jp:
        if car not in ["(",")",","]:
            id_jp = car
    query4 = '''INSERT INTO produitjardinspartages ( idProduit, idJardin) VALUES (?, ?)'''
    args4=[id_prod,id_jp,]
    cursor4=db.cursor()
    cursor4.execute(query4,args4)
    db.commit()
    path = "img/"+str(nom_fichier)
    query5='''INSERT INTO imageproduit (idProduit,Path) VALUES (?,?)'''
    args5=[id_prod,path]
    cursor5=db.cursor()
    cursor5.execute(query5,args5)
    db.commit()