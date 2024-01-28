from flask import Flask , render_template , request , redirect , g , url_for,flash
from flask import session
import modules.bdd as bdd

def amap_form():
    i=0
    res=[]
    lat_user = session['connexion']['latitude']
    long_user = session['connexion']['longitude']
    query2 = '''SELECT * FROM AMAP join locations on locations.idLocation = AMAP.idLocation '''
    cursor2 = bdd.get_db().cursor()
    cursor2.execute(query2)
    data = cursor2.fetchall()
    for item in data:
        l = list(item)
        dist = bdd.distance(lat_user,long_user, float(item[9]),float(item[10]))
        l.append(dist)
        i+=1
        res.append(l)
    return res

def amap_solo(id):
    query = '''SELECT * from AMAP where id = ?'''
    arg = [id,]
    cursor = bdd.get_db().cursor()
    cursor.execute(query,arg)
    data = cursor.fetchall()
    return data