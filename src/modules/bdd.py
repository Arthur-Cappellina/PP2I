from sqlalchemy import create_engine
from sqlalchemy.sql import text
import sqlite3
import math
from flask import g
from geopy.geocoders import Nominatim
geocoder = Nominatim(user_agent="OpenStreetMap Nominatim")


DATABASE='database/database.db'

# cette fonction permet de créer une connexion à la base
# ou de récupérer la connexion existante
def get_db(): 
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception): # pour fermer la connexion proprement
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Méthode permettant de faire un select de marnière générique 
# Exemple : print(bdd.select("user", ["username", "password"])) renverra le résultat de : 
# SELECT username,password FROM user
def select(table, attributs=["*"], conditions={}, limit=0, tables_jointes={}, distinct="", order="", connector=" AND"): 
    # On créé ici le début de la requête avec les différents attributs que l'on souhaire récupérer
    params_str = ""
    for a in attributs:
        params_str += a + "," 
    params_str = params_str[:-1]
    # On créé la requête
    request = "SELECT " + distinct + " " + params_str + " FROM " + table
    if len(tables_jointes) > 0: 
        for t in tables_jointes: 
            request += " JOIN " + t + " ON " + tables_jointes[t]

    # Si l'utilisateur a ajouté des conditions, on sélectionne uniquement avec les contraintes 
    if len(conditions) > 0: 
        request = request + " WHERE "
        for c in conditions:
            request += " " + c  + "= :" + c + connector
        request = request[:-3] + order
        engine = create_engine('sqlite:///' + DATABASE)
        con = engine.connect()
        query = text(request + addLimit(limit))
        res = con.execute(query, conditions)
        return res.fetchall()
    
    request = request + order + addLimit(limit)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(request)
    res = cur.fetchall()
    return res

def insert(table,attributs=[],valeurs=['*'],limit=0):
    #début de la requete
    param_req = ""
    for a in attributs:
        param_req += a + ","
    param_req = param_req[:-1]
    valeur_req = ""
    interro = "("
    for v in valeurs:
        valeur_req += v + ","
        interro += "?,"
    valeur_req = valeur_req[:-1]        
    interro = interro[:-1] + ")"
    #crée la requête
    if len(attributs) > 0:
        request = "INSERT INTO " + table + "(" + param_req + ")" + "VALUES" +  '(' + valeur_req + ')'
    else: 
        request = "INSERT INTO " + table + " VALUES " + interro 
    request = request + addLimit(limit)
    connnexion = sqlite3.connect(DATABASE)
    cursor = connnexion.cursor()
    cursor.execute(request, tuple(valeurs))
    connnexion.commit()

def delete(table,conditions={},limit=0):
    conditions_req = ""
    for c in conditions:
        conditions_req += c + ","
    conditions_req = conditions_req[:-1]
    request = "DELETE FROM" + table + "WHERE"
    for c in conditions_req:
        request += " " + c  + "= :" + c + " AND"
    request = request[:-3]
    engine = create_engine('sqlite:///' + DATABASE)
    con = engine.connect()
    query = text(request + addLimit(limit))
    res = con.execute(query, conditions)
    
def update(table,attribut=['*'],new_values=['*'],difference="",conditions={},limit=0):
    request = "UPDATE "+ table + " SET "
    for i in range(len(attribut)):
        request+= attribut[i] + "=" + str(new_values[i]) + difference + ","
    request = request[:-1]
    if len(conditions)>0:
        request = request + " WHERE "
        for c in conditions:
            request += " " + c  + "= :" + c + " AND"
        request = request[:-3]
        engine = create_engine('sqlite:///' + DATABASE)
        con = engine.connect()
        query = text(request + addLimit(limit))
        res = con.execute(query, conditions)
        return
    request = request + addLimit(limit)
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(request)
    con.commit()
    cur.close()

def insert_loc(adresse,la,lo):
    engine = create_engine("sqlite:///" + DATABASE)
    con = engine.connect()
    statement = text('INSERT INTO locations(adresse,latitude,longitude) VALUES (:a, :la, :lo)')
    con.execute(statement, {'a': adresse, 'la': la, 'lo': lo})
    con.close()

def insert_user(email,pseudo,password,idlocation):
    engine = create_engine("sqlite:///" + DATABASE)
    con = engine.connect()
    statement = text('INSERT INTO USER(email,pseudo,password,idlocation,status) VALUES (:a, :b, :c, :d, :e)')
    con.execute(statement, {'a': email, 'b': pseudo, 'c': password, 'd': idlocation, 'e': 'user'})
    con.close()

def insert_code(code):
    engine = create_engine("sqlite:///" + DATABASE)
    con = engine.connect()
    statement = text('INSERT INTO codeconfirmation(code) VALUES (:a)')
    con.execute(statement, {'a': code})
    con.close()

def insert_jardin(owner_id,name,description,idlocation):
    engine = create_engine("sqlite:///" + DATABASE)
    con = engine.connect()
    statement = text('INSERT INTO jardinpartage(ownerId,name,description,idlocation) VALUES (:a, :c, :d, :e)')
    con.execute(statement, {'a': owner_id, 'c': name, 'd': description, 'e': idlocation})
    con.close()

def insert_image_jardin(idjardin,path):
    engine = create_engine("sqlite:///" + DATABASE)
    con = engine.connect()
    statement = text('INSERT INTO imagejardin(idjardin,path) VALUES (:a, :b)')
    con.execute(statement, {'a': idjardin, 'b': path})
    con.close()

def insert_ferme(owner_id,name,description,idlocation):
    engine = create_engine("sqlite:///" + DATABASE)
    con = engine.connect()
    statement = text('INSERT INTO microferme(ownerId,nom,description,idlocation) VALUES (:a, :c, :d, :e)')
    con.execute(statement, {'a': owner_id, 'c': name, 'd': description, 'e': idlocation})
    con.close()

def insert_image_ferme(idferme,path):
    engine = create_engine("sqlite:///" + DATABASE)
    con = engine.connect()
    statement = text('INSERT INTO imageferme(idferme,path) VALUES (:a, :b)')
    con.execute(statement, {'a': idferme, 'b': path})
    con.close()

#entrée : latitude de la forme : 31.54012541'
#longitude de la forme : 31.54012541'
def distance(lat1,long1,lat2,long2):
    r = 6378137
    lat1rad = lat1/180*math.pi
    lat2rad = lat2/180*math.pi
    long1rad = long1/180*math.pi
    long2rad = long2/180*math.pi
    inte = math.sin(lat1rad)*math.sin(lat2rad)+math.cos(lat1rad)*math.cos(lat2rad)*math.cos(abs(long2rad-long1rad))
    dist_point = r*math.acos(inte)
    return round(dist_point/1000,2)


def conv_adresse_to_GPS(adresse):
    location = geocoder.geocode(adresse)
    if location != None:
        return (location.latitude,location.longitude)
    else :
        return "Adresse non trouvé"


def addLimit(n): 
    return "" if n == 0 else " LIMIT " + str(n)




