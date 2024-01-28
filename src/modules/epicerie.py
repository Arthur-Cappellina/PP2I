from flask import Flask , render_template , request , redirect , g , url_for,flash
from flask import session
import modules.bdd as bdd

app = Flask(__name__)
app.secret_key = b"6702ffe5d5961ebe3fd3fd13ced7562b33d1db40478d49d3cef58678dbbb8c09"

def epicerie():
    if request.method == 'GET' :
        adresse = ''
        distance = ''
    else :
        distance = request.form['distance']
        adresse = request.form['adresse']
    if distance == '' :
        distance = 10
    else :
        distance = float(distance)
    if adresse == '' and session.get('logged_in') != True :
        msg = 0
        return msg
    elif adresse == '' and session.get('logged_in') == True:
        la = session['connexion']['latitude']
        lo = session['connexion']['longitude']
    else :
        location = bdd.conv_adresse_to_GPS(adresse)
        if location == "Adresse non trouvé" :
            msg = 1
            return msg
        la = location[0]
        lo = location[1]
    data1=bdd.select("JardinPartage", ["id,latitude,longitude"],tables_jointes={"locations": "JardinPartage.idLocation = locations.idLocation"})
    data2=bdd.select("User", ["id,latitude,longitude"],tables_jointes={"locations": "User.idLocation = locations.idLocation"})
    data3=bdd.select("Microferme", ["id,latitude,longitude"],tables_jointes={"locations": "Microferme.idLocation = locations.idLocation"})
    data=[]
    for i in range(len(data1)):
        if bdd.distance(data1[i][1],data1[i][2],la,lo)<distance:
            data.append([data1[i][0],"ProduitJardinsPartages"])
    for i in range(len(data2)):
        if bdd.distance(data2[i][1],data2[i][2],la,lo)<distance:
            data.append([data2[i][0],"ProduitUser"])
    for i in range(len(data3)):
        if bdd.distance(data3[i][1],data3[i][2],la,lo)<distance:
            data.append([data3[i][0],"ProduitMicroFerme"])
    idproduit = []
    for i in data :
        data0=[]
        if i[1]=="ProduitJardinsPartages" :
            data0=bdd.select("ProduitJardinsPartages",["idproduit"],conditions={"idJardin": i[0]})
        elif i[1]=="ProduitUser" :
            data0=bdd.select("ProduitUser",["idproduit"],conditions={"idUser": i[0]})
        elif i[1]=="ProduitMicroFerme" :
            data0=bdd.select("ProduitMicroFerme",["idproduit"],conditions={"idMicroferme": i[0]})
        for j in data0 :
            idproduit.append(j[0])
    data_produit=[]
    path=[]
    for i in idproduit :
        data_produit_i=bdd.select("Produit",["*"],conditions={"id": i,})
        print(data_produit_i)
        if data_produit_i[0][-2]=='ok':
            data_produit.append(data_produit_i)
            path.append(bdd.select("ImageProduit",["path"],conditions={"idProduit": i}))
    return data_produit,path