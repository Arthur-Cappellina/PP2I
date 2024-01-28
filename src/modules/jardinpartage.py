import sqlite3
from flask import Flask , render_template , request , redirect , g , url_for,flash
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
import random 

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


def selectproduit(idJardin):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("SELECT id,name,typeProduit,Produit.quantite,prix,description FROM Produit JOIN ProduitJardinsPartages ON ProduitJardinsPartages.idProduit=Produit.id WHERE idJardin=:id" , {"id": idJardin})
    data_produit=cur.fetchall()
    con.commit()
    con.close()
    Image=[]
    for i in range(len(data_produit)):
        idproduit=data_produit[i][0]
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute("SELECT path FROM ImageProduit WHERE idProduit=:id" , {"id": idproduit})
        image=cur.fetchall()
        con.commit()
        con.close()
        Image.append(image)
    return data_produit,Image    
