import modules.bdd as bdd
from flask import Flask , render_template , request , redirect , g , url_for,flash
from flask_mail import Mail, Message
from flask import session

app = Flask(__name__)
app.secret_key = b"6702ffe5d5961ebe3fd3fd13ced7562b33d1db40478d49d3cef58678dbbb8c09"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'potagix372@gmail.com'
app.config['MAIL_PASSWORD'] = 'erxyotnvhtfowrne'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


def admin_get():
    query = '''SELECT Produit.typeProduit,Produit.prix,Produit.description, ImageProduit.path, horaires.dateHeures, horaires.debut, horaires.fin, Produit.name, Produit.id FROM Produit
    join ImageProduit on ImageProduit.idProduit = Produit.id join horaires on horaires.idHeure = Produit.idHeure WHERE valid = "non" and display = 1'''
    cursor = bdd.get_db().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    query2 = '''SELECT user.pseudo,transactions.cagnotte_temp,transactions.id_user,transactions.id_transaction FROM transactions join user on transactions.id_user = user.id WHERE valide = 0'''
    cursor2 = bdd.get_db().cursor()
    cursor2.execute(query2)
    data2 = cursor2.fetchall()
    print(data2)
    return data,data2

def admin_post_ok(id_prod):
    query1 ='''UPDATE produit SET valid = 'ok' WHERE id = ?'''
    arg1 = [id_prod]
    db = bdd.get_db()
    cursor = db.cursor()
    cursor.execute(query1,arg1)
    db.commit()
    
def first(id_prod):
    query2 = '''SELECT idUser FROM produituser WHERE idProduit = ?'''
    arg2 = [id_prod]
    cursor2 = bdd.get_db().cursor()
    cursor2.execute(query2,arg2)
    first = cursor2.fetchall()
    return first

def second(id_prod):
    query3 = '''SELECT ownerId FROM jardinpartage join produitjardinspartages on jardinpartage.id = produitjardinspartages.idJardin
    join produit on produit.id = produitjardinspartages.idProduit WHERE Produit.id = ?'''
    arg3 = [id_prod]
    cursor3 = bdd.get_db().cursor()
    cursor3.execute(query3,arg3)
    second = cursor3.fetchall()
    return second

def third(id_prod):
    query4='''SELECT ownerId FROM microferme join produitmicroferme on microferme.id = produitmicroferme.idMicroFerme join produit 
    on produit.id = produitmicroferme.idProduit WHERE produit.id = ?'''
    arg4 = [id_prod]
    cursor4 = bdd.get_db().cursor()
    cursor4.execute(query4,arg4)
    third = cursor4.fetchall()
    return third

def send_first(l):
    id = 0
    email=''
    for car in l:
        if car not in ["(",")",","]:
            id = car 
    query5 = '''SELECT email FROM user WHERE id = ?'''
    arg5 = [id[0]]
    cursor5=bdd.get_db().cursor()
    cursor5.execute(query5,arg5)
    string_email = cursor5.fetchall()[0]
    for car in string_email:
        if car not in ["(",")",","]:
            email = email + car 
    msg = Message("Proposition d'un produit non conforme",
    sender="potagix372@gmail.com",
    recipients=[email])
    msg.body = "Votre produit n'a pas été accepté. Veuillez compléter à nouveau le formulaire pour proposer votre produit."
    mail.send(msg)
    
def dysplay_cache(id):
    query = '''UPDATE produit SET display = 0 where id = ?'''
    arg = [id,]
    db = bdd.get_db()
    cursor = db.cursor()
    cursor.execute(query,arg)
    db.commit()
    

def transact(solde,id,id_transaction):
    query = '''UPDATE User SET cagnotte = cagnotte + ? WHERE id = ?'''
    arg = [solde,id]
    db = bdd.get_db()
    cursor = db.cursor()
    cursor.execute(query,arg)
    db.commit()
    query2 = '''UPDATE transactions SET valide = 1 WHERE id_transaction = ? '''
    arg2 = [id_transaction]
    cursor2 = db.cursor()
    cursor2.execute(query2,arg2)
    db.commit()
    
def save_session():
    pseudo = session['connexion']['pseudo']
    latitude = session['connexion']['latitude']
    longitude = session['connexion']['longitude']
    idLocation = session['connexion']['idlocation']
    cagnotte = bdd.select("user",['cagnotte'], conditions={"pseudo":pseudo})
    session.pop('connexion')
    session['connexion'] = {
            'pseudo': pseudo,
            'latitude': latitude,
            'longitude': longitude,
            'idlocation': idLocation,
            'cagnotte': cagnotte[0][0]
        }