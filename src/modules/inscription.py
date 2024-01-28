from flask import Flask , render_template , request , redirect , g , url_for,flash
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
from flask import session
import random 
import modules.bdd as bdd

app = Flask(__name__)
app.secret_key = b"6702ffe5d5961ebe3fd3fd13ced7562b33d1db40478d49d3cef58678dbbb8c09"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'potagix372@gmail.com'
app.config['MAIL_PASSWORD'] = 'erxyotnvhtfowrne'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def inscrire():
    if request.method == 'GET' :
        msg=0
    else :
        email = request.form['email']
        adresse = request.form['adresse']
        pseudo = request.form['pseudo']
        data_pseudo = bdd.select("user", ["pseudo"], conditions={"pseudo": pseudo})
        data_email = bdd.select("user", ["email"], conditions={"email": email})
        location = bdd.conv_adresse_to_GPS(adresse)
        if len(email)==0 :
            msg=6
        elif len(data_pseudo)!=0:
            msg=2
        elif len(request.form['password'])<8:
            msg=3
        elif len(data_email)!=0:
            msg=4
        elif location == "Adresse non trouvé" :
            msg=5
        else :
            distance=bdd.distance(48.692054,6.184417,float(location[0]),float(location[1]))
            print(distance,"et ho")
            msg=True
            password = sha256_crypt.encrypt(request.form['password'])
            message = Message("Confirmation inscription",
                        sender="potagix372@gmail.com",
                        recipients=[email])
            number=''
            for i in range(6):
                number+=str(random.randint(0,9))
            message.body = "Bonjour, le code d'autentification est : "+number
            mail.send(message)
            bdd.insert_code(sha256_crypt.encrypt(number))
            idcode=(bdd.select('codeconfirmation',['max(id)']))[0][0]
            session['inscription'] = {
                'pseudo': pseudo,
                'location': location, 
                'adresse': adresse,
                'email': email,
                'password': password,
                'id': idcode
            }
    print("msg",msg)
    return msg

def confirmer_inscription():
    if request.method == 'GET' :
        msg=0
    else :
        code = (bdd.select('codeconfirmation',['code'],conditions={'id': session['inscription']['id']}))[0][0]
        if not sha256_crypt.verify(request.form['number'], code) :
            msg=2
        else :
            print("codeok")
            msg=True
            location = session['inscription']['location']
            la = str(location[0])
            lo = str(location[1])
            adresse = session['inscription']['adresse']
            email = session['inscription']['email']
            pseudo = session['inscription']['pseudo']
            password = session['inscription']['password']
            bdd.insert_loc(adresse,la,lo)
            idlocation=bdd.select("locations", ["max(idLocation)"], conditions={"adresse": adresse})
            idlocation=int(idlocation[0][0])
            bdd.insert_user(email,pseudo,password,idlocation)
            session.pop('inscription')

    return msg

def connexion1():
    if request.method == 'GET' :
        msg = 0
    else :
        pseudo = request.form['pseudo']
        password = request.form['password']
        bon_mdp=(bdd.select("user", ["password"], conditions={"pseudo": pseudo}))
        if len(bon_mdp)==0 or not sha256_crypt.verify(password, bon_mdp[0][0]) :
            msg=1
        else :
            cagnotte = bdd.select("user",['cagnotte'], conditions={"pseudo":pseudo})
            print(cagnotte)
            location=bdd.select("user", ["latitude,longitude,locations.idLocation"],tables_jointes={"locations": "user.idLocation = locations.idLocation"}, conditions={"pseudo": pseudo})
            session['logged_in'] = True
            session['connexion'] = {
                'pseudo': pseudo,
                'latitude': location[0][0],
                'longitude': location[0][1],
                'idlocation': location[0][2],
                'cagnotte': cagnotte[0][0]
            }
            msg = 2
    return msg


