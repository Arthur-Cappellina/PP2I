from flask import Flask , render_template , request , redirect , g , url_for,flash
from flask import session
import modules.bdd as bdd
import os
from werkzeug.utils import secure_filename
import random
import string

UPLOAD_FOLDER = '/static/img'
ALLOWED_EXTENSIONS = {'jpeg','png','jpg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def nom_fichier_image():
    length=random.randint(25,100)
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(length))+'.png'

def jardin(nom_fichier_img):
    if session.get('logged_in') != True :
        return 3
    owner_id=(bdd.select('user',['id'],conditions={'pseudo': session['connexion']['pseudo']}))[0][0]
    if len(bdd.select('jardinpartage',['id'],conditions={'ownerId': owner_id})) != 0:
        return 6
    if request.method == 'GET' :
        return 0
    name = request.form['name']
    description = request.form['description']
    file = request.files['file']
    adresse = request.form['adresse']
    location = bdd.conv_adresse_to_GPS(adresse)
    if name == '' or description == '' or 'file' not in request.files or file.filename == '' :
        return 1
    if not file or not allowed_file(file.filename):
        return 5        
    if len(name) > 256 or len(description) > 256 :
        return 2
    if location == "Adresse non trouvé" :
        return 7
    la = str(location[0])
    lo = str(location[1])
    bdd.distance(48.692054,6.184417,la,lo)
    bdd.insert_loc(adresse,la,lo)
    idlocation=(bdd.select('locations',["max(idLocation)"]))[0][0]
    path="static/"+nom_fichier_img
    bdd.insert_jardin(owner_id,name,description,idlocation)
    idjardin=(bdd.select('jardinpartage',['id'],conditions={'ownerId': owner_id}))[0][0]
    bdd.insert_image_jardin(idjardin,path)
    return 4,file,nom_fichier_img
            
def ferme(nom_fichier_img):
    if session.get('logged_in') != True :
        return 3
    owner_id=(bdd.select('user',['id'],conditions={'pseudo': session['connexion']['pseudo']}))[0][0]
    if len(bdd.select('microferme',['id'],conditions={'ownerId': owner_id})) != 0:
        return 6
    if request.method == 'GET' :
        return 0
    name = request.form['name']
    description = request.form['description']
    file = request.files['file']
    adresse = request.form['adresse']
    location = bdd.conv_adresse_to_GPS(adresse)
    if name == '' or description == '' or 'file' not in request.files or file.filename == '' :
        return 1
    if not file or not allowed_file(file.filename):
        return 5        
    if len(name) > 256 or len(description) > 256 :
        return 2
    if location == "Adresse non trouvé" :
        return 7
    la = str(location[0])
    lo = str(location[1])
    bdd.distance(48.692054,6.184417,la,lo)
    bdd.insert_loc(adresse,la,lo)
    idlocation=(bdd.select('locations',["max(idLocation)"]))[0][0]
    path="static/"+nom_fichier_img
    bdd.insert_ferme(owner_id,name,description,idlocation)
    idferme=(bdd.select('microferme',['id'],conditions={'ownerId': owner_id}))[0][0]
    bdd.insert_image_ferme(idferme,path)
    return 4,file,nom_fichier_img