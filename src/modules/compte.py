from flask import Flask , render_template , request , redirect , g , url_for,flash
from flask import session
import modules.bdd as bdd
import random 
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = b"6702ffe5d5961ebe3fd3fd13ced7562b33d1db40478d49d3cef58678dbbb8c09"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'potagix372@gmail.com'
app.config['MAIL_PASSWORD'] = 'erxyotnvhtfowrne'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def cgh():
    pseudo_act = session['connexion']['pseudo']
    new_name = request.form['name']
    query='''UPDATE User SET pseudo = ? where pseudo = ?'''
    args = [new_name,pseudo_act,]
    db = bdd.get_db()
    cursor = db.cursor()
    cursor.execute(query,args)
    db.commit()
    
    
def cgh_email():
    new_adresse = request.form['name']
    msg = Message("Confirmation changement adresse mail",
              sender="potagix372@gmail.com",
              recipients=[new_adresse])
    number=''
    for i in range(6):
        number+=str(random.randint(0,9))
    msg.body = "Bonjour, le code d'autentification est : "+number
    mail.send(msg)
    session['changement'] = {
        'pseudo': session['connexion']['pseudo'],
        'new_email': new_adresse,
        'number': sha256_crypt.encrypt(number)
    }

def conf_cgh_email():
    new_adresse = session['changement']['new_email']
    pseudo = session['connexion']['pseudo']
    query ='''UPDATE User SET email = ? WHERE pseudo = ? '''
    args = [new_adresse,pseudo,]
    db = bdd.get_db()
    cursor = db.cursor()
    cursor.execute(query,args)
    db.commit()
    
    
def cgh_adresse():
    id_user = 0
    new_adresse = request.form['name']
    pseudo = session['connexion']['pseudo']
    query1 = '''SELECT locations.idlocation from locations join User on User.id = locations.idlocation WHERE pseudo = ?'''
    arg1=[pseudo,]
    cursor1 = bdd.get_db().cursor()
    cursor1.execute(query1,arg1)
    string = cursor1.fetchall()[0]
    for car in string:
        if car not in ["(",")",","]:
            id_user = car
    new_lat,new_long = bdd.conv_adresse_to_GPS(new_adresse)
    query = '''UPDATE locations SET adresse = ?, latitude = ?, longitude = ? WHERE idlocation = ? '''
    args = [new_adresse,new_lat,new_long,id_user,]
    db = bdd.get_db()
    cursor2 = db.cursor()
    cursor2.execute(query,args)
    db.commit()
    
    
def ajout(id,nom_fichier):
    name = session['connexion']['pseudo']
    path = "img/"+str(nom_fichier)
    query = '''SELECT id from User WHERE pseudo = ?'''
    arg = [name,]
    cursor = bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id = cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car            
    query2 = '''UPDATE User SET imageProfil = ? WHERE id = ?'''
    arg2 = [path,id]
    db = bdd.get_db()
    cursor2 = db.cursor()
    cursor2.execute(query2,arg2)
    db.commit()
    
def display():
    user = bdd.select("User",conditions={"pseudo":session['connexion']['pseudo']})[0]
    adresse = bdd.select("locations",conditions={"idlocation":user[7]})[0]
    data = {
        "pseudo":user[1],
        "email":user[2],
        "adresse":adresse[2],
        "image": user[5]
    }
    return data

def type_compte():
    id = 0
    status = ''
    name = session['connexion']['pseudo']
    query='''SELECT id FROM User WHERE pseudo = ?'''
    arg = [name,]
    cursor = bdd.get_db().cursor()
    cursor.execute(query,arg)
    string_id = cursor.fetchall()[0]
    for car in string_id:
        if car not in ["(",")",","]:
            id = car 
    query2='''SELECT status FROM User WHERE id = ?'''
    arg2=[id,]
    cursor2 = bdd.get_db().cursor()
    cursor2.execute(query2,arg2)
    string_status = cursor2.fetchall()[0]
    for car in string_status:
        if car not in ["(",")",","]:
            status = status + car 
    return status

def param_compte():
    user = bdd.select("User",conditions={"pseudo":session['connexion']['pseudo']})[0]
    adresse = bdd.select("locations",conditions={"idlocation":user[7]})[0]
    data = {
        "pseudo":user[2],
        "email":user[1],
        "adresse":adresse[1],
        "cagnotte":user[8],
        "image": user[5]
    }
    return data

def produit_sauve():
    pseudo = session['connexion']['pseudo']
    id = bdd.select("user",['id'], conditions={"pseudo":pseudo})
    prod = bdd.select('commande',conditions={'buyerId':id[0][0]})
    return len(prod)

def prod_donnees():
    pseudo = session['connexion']['pseudo']
    id = bdd.select("user",['id'], conditions={"pseudo":pseudo})
    first = bdd.select('commande',tables_jointes={'produit': "commande.idProduit = produit.id",'produituser': 'produituser.idProduit=produit.id'},conditions={'idUser':id[0][0]})
    second = bdd.select('commande',tables_jointes={'produit': "commande.idProduit = produit.id",'produitmicroferme': "produitmicroferme.idProduit = produit.id","Microferme":"Microferme.id=produitmicroferme.idMicroFerme"},
    conditions = {'ownerId':id[0][0]})
    third = bdd.select('commande',tables_jointes={'produit': "commande.idProduit = produit.id","produitjardinspartages":"produitjardinspartages.idProduit=produit.id","jardinpartage":"jardinpartage.id=produitjardinspartages.idJardin"},
    conditions = {'ownerId': id[0][0]})
    return len(first)+len(second)+len(third)