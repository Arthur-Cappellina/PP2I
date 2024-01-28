# Fichier qui s'occupe de stocker toutes les routes et d'appeler des méthode dans des modules pour afficher ces routes 
import modules.bdd as bdd
import modules.user as user
import modules.map as map
import modules.inscription as ins
import modules.accueil as accueil
import modules.produit as produit
import modules.creer as creer
import modules.epicerie as epicerie
from flask import Flask , render_template , request , redirect , g , url_for,flash, session ,json
from passlib.hash import sha256_crypt
from flask_mail import Mail, Message
import random 
from werkzeug.utils import secure_filename
import os
import modules.amap as am
import modules.compte as cmpt
import modules.graine as grn
import modules.admin as ad
import modules.informations as informations
import modules.vos_prod as vp
import modules.prop as prop
import modules.config as conf
import modules.cagnotte as ca
import modules.commande as comm
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

mail = conf.setup(app)

@app.errorhandler(HTTPException)
def handle_exception(e):
    return render_template("erreur.html")

def fichierauto(namefichier):
    extension = namefichier.split('.')[-1]
    return (extension in {'jpg','jpeg','png'})
###
@app.route('/accueil')
def home():
    return render_template("accueil.html", data=accueil.get_data())

@app.route('/map')
def mapIt():
    print(map.get_map_data(request)["nearPoints"][0])
    return render_template("map.html", data=map.get_map_data(request))

@app.route('/produit/<id>', methods=['GET','POST'])
def get_produit(id):
    try:
        return render_template("produit.html", data=produit.get_data_formatted(id, request))
    except:
        return render_template("erreur.html", erreur="Le produit n'a pas été trouvé")        
        


@app.route('/panier', methods=['GET','POST'])
def panier():
    if len(request.args) > 0 and "delete" in request.args:
        del session["panier"][request.args["delete"]]
        session.modified = True
        return redirect(request.url_root + "panier")
    return render_template("panier.html", data=produit.get_product_cart(request))

@app.route('/micro-ferme/<id>', methods=['GET'])
def microferme(id): 
    try: 
        return render_template("informations.html", data=informations.get_data(id))
    except:
        return render_template('erreur.html', erreur="micro ferme non trouvée")

@app.route('/jardin-partage/<id>', methods=['GET'])
def jardinpartage(id):
    try:
        return render_template("informations.html", data=informations.get_data_jardin(id))
    except:
        return render_template('erreur.html', erreur="jardin partagé non trouvé")

@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    return render_template("informations.html", data=informations.get_data_user(id))


@app.route('/mon-compte')
def getUser():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method == 'GET' and len(request.args) > 0 and request.args['query'] == "deconnexion": 
        session.clear()
        return redirect("accueil")
    data = cmpt.param_compte()
    prod_sau = cmpt.produit_sauve()
    prod_donn = cmpt.prod_donnees()
    return render_template('utilisateur.html', status=cmpt.type_compte(), data = data,save = prod_sau,given=prod_donn)
    

@app.route('/admin', methods=['GET','POST'])
def admin():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method=='GET':
        data,data2 = ad.admin_get()
        return render_template('page_admin.html',data = data, data2 = data2)
    elif request.method=='POST':
        id_prod = request.form['id-prod']
        choice = request.form['Btn']
        if choice == 'ok':
            ad.admin_post_ok(id_prod)
            return redirect(url_for('admin'))
        if choice == 'non':
            first = ad.first(id_prod)
            second = ad.second(id_prod)
            third = ad.third(id_prod)
            if first != []:
                ad.dysplay_cache(id_prod)
                ad.send_first(first)
            if second != []:
                ad.dysplay_cache(id_prod)
                ad.send_first(second)
            if third != []:
                ad.dysplay_cache(id_prod)
                ad.send_first(third)
            return redirect(url_for('admin'))

@app.route('/admin-transaction', methods=['POST'])
def admin_transac():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method == 'POST':
        solde = request.form.get('solde')
        id = request.form.get('id')
        choice = request.form['Btn']
        print(id)
        id_transaction = request.form.get('id_transact')
        if choice == 'ok':
            ad.transact(solde,id,id_transaction)
            ad.save_session()
            return redirect(url_for('admin'))

@app.route('/proposition', methods=['GET','POST'])
def proposition():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method=='POST':
        file_up = request.files['file']
        if file_up.filename == '':
            flash('Pas de fichier sélectionné')
            return redirect(url_for('proposition'))
        if file_up and fichierauto(file_up.filename):
            choice = request.form['Btn']
            structure = request.form['Btn2']
            price = request.form.get('prix')
            quantite = request.form.get('quantite')
            nom_prod = request.form.get('nom_produit')
            description= request.form.get('description')
            date_collecte = request.form.get('schedule')
            debut_collecte = request.form.get('debut')
            fin_collecte = request.form.get('fin')
            name = session['connexion']['pseudo']
            nom_fichier = secure_filename(file_up.filename)
            while not nom_fichier_valide(nom_fichier):
                nom_fichier=creer.nom_fichier_image()
            file_up.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier))
            if structure=='particulier':
                prop.propo_part(date_collecte,debut_collecte,fin_collecte,name,choice,price,description,nom_prod,quantite,nom_fichier)
                return redirect(url_for('enregistre'))
            if structure == 'Micro Ferme':
                prop.propo_micro(date_collecte,debut_collecte,fin_collecte,name,choice,price,description,nom_prod,quantite,nom_fichier)
                return redirect(url_for('enregistre'))
            if structure == 'Jardin Partagé':
                prop.propo_jardin(date_collecte,debut_collecte,fin_collecte,name,choice,price,description,nom_prod,quantite,nom_fichier)
                return redirect(url_for('enregistre'))
    elif request.method == 'GET':
        return render_template('prop_prod.html')

@app.route('/enregistre')
def enregistre():
    return render_template('enregistre.html')

@app.route('/compte')
def compte():
    if not user.isConnected():
        return render_template('not_connected.html')
    data = cmpt.display()
    return render_template('param_compte.html',pseudo = data["pseudo"], email = data["email"], adresse = data["adresse"], image=data["image"])


@app.route('/amap', methods = ['GET','POST'])
def amap():
    if not user.isConnected(): 
        return render_template('not_connected.html')
    if request.method=='GET':
        res = am.amap_form()
        return render_template('amap.html', data = res)
    
    
@app.route('/amap/<id>', methods=['GET'])
def uniqueamap(id):
    try:
        return render_template('uniqueAmap.html', item = am.amap_solo(id)[0])
    except:
        return render_template('erreur.html', erreur="amap non trouvée")

@app.route('/vos-produits',methods=['GET','POST'])
def vos_produits():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method=='GET':
        return render_template('vos_prod.html')
    elif request.method=='POST':
        prod = request.form['Btn']
        if prod=='particulier':
            data = vp.prod_parti()
            return render_template('vos_prod.html',data=data)
        if prod=='Jardin Partagé':
            data = vp.prod_jardin()
            return render_template('vos_prod.html',data=data)  
        if prod=='Micro Ferme':
            data = vp.prod_micro()
            return render_template('vos_prod.html',data=data)  

@app.route('/modifier-pseudo', methods=['GET','POST'])
def chg():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method =='GET':
        return render_template('chg.html')
    elif request.method =='POST':
        cmpt.cgh()
        return redirect(url_for('connexion'))


@app.route('/modifier-email', methods=['GET','POST'])
def chg_email():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method=='GET':
        return render_template('chg_email.html')
    elif request.method=='POST':
        cmpt.cgh_email()
        return redirect(url_for('confirmation_chg_email'))

@app.route('/confirmation-changement-email', methods=['GET','POST'])
def confirmation_chg_email():
    if request.method == 'GET' :
        return render_template('chg_email_confirmation.html',msg=0)
    elif not sha256_crypt.verify(request.form['number'], session['changement']['number']) :
        return render_template('chg_email_confirmation.html',msg=1)
    else:
        cmpt.conf_cgh_email()
        return redirect(url_for('compte'))
    
@app.route('/modifier-adresse', methods = ['GET','POST'])
def chg_adresse():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method=='GET':
        return render_template('chg_adresse.html')
    elif request.method=='POST':
        cmpt.cgh_adresse()
        return redirect(url_for('connexion'))
    
@app.route('/ajout',methods=['GET','POST'])
def ajout():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method == 'GET':  
        return render_template("ajout_avatar.html")
    elif request.method == 'POST':
        file_up = request.files['file']
        if file_up and fichierauto(file_up.filename):
            id = 0
            nom_fichier = secure_filename(file_up.filename)
            while not nom_fichier(nom_fichier):
                nom_fichier=creer.nom_fichier_image()
            file_up.save(os.path.join(app.config['UPLOAD_FOLDER'], nom_fichier))
            cmpt.ajout(id,nom_fichier)
            return redirect(url_for('compte'))          


@app.route('/graine', methods=['GET','POST'])
def graine():
    if request.method=='GET':
        month,data = grn.graine_get()
        return render_template('graine.html',data=data, mois=month)
    elif request.method=='POST':
        month,data = grn.graine_post()
        return render_template('graine.html',data=data, mois=month)


@app.route('/')
def hello():
    return redirect('/accueil')

@app.route('/inscription',methods=['GET','POST'])
def inscription():
    if session.get('logged_in') :
        return render_template('already_connected.html')
    msg=ins.inscrire()
    if msg == True :
        return redirect('/confirmation-inscription')
    else :
        return render_template('inscription.html',msg=msg)

@app.route('/confirmation-inscription',methods=['GET','POST'])
def confirmation_inscription():
    if session.get('logged_in') :
        return render_template('already_connected.html')
    msg=ins.confirmer_inscription()
    if msg == True :
        return render_template('inscrit.html')
    else :
        return render_template('confirmation_inscription.html',msg=msg)
                        

@app.route('/connexion',methods=['GET','POST'])
def connexion():
    if session.get('logged_in') :
        return render_template('already_connected.html')
    msg=ins.connexion1()
    if msg == 2 :
        return redirect(url_for('home'))
    else :
        return render_template('connexion.html',msg=msg)

@app.route('/epicerie-virtuelle',methods=['GET','POST'])
def epicerievirtuelle():
    data=epicerie.epicerie()
    if data == 0 or data == 1 :
        return render_template("epicerie.html",msg=data)
    else :
        return render_template('epicerie.html',data=data[0], path=data[1])

@app.route('/creer-jardin',methods=['GET','POST'])
def creer_jardin():
    if not user.isConnected():
        return render_template('not_connected.html')
    nom_fichier_image=creer.nom_fichier_image()
    while not nom_fichier_valide(nom_fichier_image):
        nom_fichier_image=creer.nom_fichier_image()
    msg=creer.jardin(nom_fichier_image)
    if type(msg) == int :
        return render_template("creer_jardin.html",msg=msg)
    else :
        msg[1].save(os.path.join(app.config['UPLOAD_FOLDER'], msg[2]))
        return render_template("creer_jardin.html",msg=msg[0])
    
@app.route('/creer-ferme',methods=['GET','POST'])
def creer_ferme():
    if not user.isConnected():
        return render_template('not_connected.html')
    nom_fichier_image=creer.nom_fichier_image()
    while not nom_fichier_valide(nom_fichier_image):
        nom_fichier_image=creer.nom_fichier_image()
    msg=creer.ferme(nom_fichier_image)
    if type(msg) == int :
        return render_template("creer_ferme.html",msg=msg)
    else :
        msg[1].save(os.path.join(app.config['UPLOAD_FOLDER'], msg[2]))
        return render_template("creer_ferme.html",msg=msg[0])

def nom_fichier_valide(nom_fichier):
    #renvoie True si le nom en argument n'est pas déjà utilisé le dossier img
    for root, directories, files in os.walk("static/img"):  
        for file in files:
            if nom_fichier==file:
                return False
    return True

@app.route('/cagnotte',methods=['GET','POST'])
def cagnotte():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method == 'GET':
        return render_template('cagnotte.html')
    if request.method == 'POST':
        somme = request.form.get('solde')
        pseudo = session['connexion']['pseudo']
        ca.cagnotte(pseudo,somme)
        return redirect(url_for('getUser'))

@app.route('/commande', methods=['GET','POST'])
def commande():
    if not user.isConnected():
        return render_template('not_connected.html')
    if request.method == 'GET':
        data = comm.commande_get()
        return render_template('commande.html',data = data)
    if request.method == 'POST':
        id_prod = request.form.get('id-prod')
        comm.commande_post(id_prod)
        return redirect(url_for('commande'))

app.run(port=5050)