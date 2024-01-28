import modules.bdd as bdd
import modules.produit as produit
from flask import session


def get_adress(name):
    first = bdd.select('user',['locations.adresse'],tables_jointes={'locations':'locations.idLocation=user.idLocation'},conditions={'pseudo': name})
    second = bdd.select('microferme',['locations.adresse'],tables_jointes={'locations':'locations.idLocation = Microferme.idLocation'},conditions={'nom': name})
    third = bdd.select('jardinpartage',['locations.adresse'],tables_jointes={'locations':'locations.idLocation = jardinpartage.idLocation'},conditions={"name": name})
    if len(first)>0:
        return first[0]
    if len(second)>0:
        return second[0]
    if len(third)>0:
        return third[0]
    
#fonction permettant de fusionner deux listes de même longueur, possédant des listes à l'intérieur de même longueur
def fuse(l1,l2):
    res = []
    temp=[]
    first = l1
    second = l2
    i = 0
    while first != []:
        for item in first :
            for word in item :
                temp.append(word)
            for word2 in second[i]:
                temp.append(word2)
            res.append(temp)
            first.pop(0)
            i+=1
            temp = []
    return res

def commande_get():
    lis = []
    adr = []
    pseudo = session['connexion']['pseudo']
    id = bdd.select('user',['id'],conditions={'pseudo':pseudo})
    donnee= bdd.select('commande',['typeProduit','prix','description','path','dateHeures','debut','fin','name','commande.quantite','produit.id'],tables_jointes={'produit':'commande.idProduit = produit.id','horaires':'Horaires.idHeure=produit.idHeure','imageproduit':'imageproduit.idProduit=produit.id'},
    conditions = {'valid':'ok','display':1,'valide':0,'buyerId':id[0][0]})
    for item in donnee:
        lis.append(produit.get_owner(item[9]))
    for item in lis:
        adr.append(get_adress(item[0]))
    data_temp = fuse(donnee,lis)
    data = fuse (data_temp,adr)
    print(donnee, id[0][0])
    return data

def commande_post(id_prod):
    query = '''UPDATE commande SET valide = 1 WHERE idProduit = ?'''
    arg = [id_prod]
    db=bdd.get_db()
    cursor=db.cursor()
    cursor.execute(query,arg)
    db.commit() 
    query2 = '''UPDATE produit SET valid = 'non' and display = 0 WHERE id = ?'''
    arg2 = [id_prod]
    cursor2 = db.cursor()
    cursor2.execute(query2,arg2)
    db.commit()