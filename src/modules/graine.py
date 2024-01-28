from datetime import datetime
import modules.bdd as bdd
from flask import Flask , render_template , request , redirect , g , url_for,flash


def graine_get():
    dico_month_inv = {"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Août",'09':"Septembre","10":"Octobre","11":"Novembre","12":"Décembre"}
    date = str(datetime.now())
    date = date.split()
    ch = date[0]
    ch = ch.split("-")
    periode = ch[1]
    month = dico_month_inv[str(periode)]
    query='''SELECT nom,image FROM Graine WHERE debut_plantation<=? and fin_plantation>=?'''
    args=(periode,periode)
    cursor = bdd.get_db().cursor()
    cursor.execute(query,args) 
    data = cursor.fetchall()
    return (month,data)

def graine_post():
    dico_month = {"Janvier":1,"Février":2,"Mars":3,"Avril":4,"Mai":5,"Juin":6,"Juillet":7,"Août":8,"Septembre":9,"Octobre":10,"Novembre":11,"Décembre":12}
    month = request.form['graine']
    periode = dico_month[month]
    query='''SELECT nom,image FROM Graine WHERE debut_plantation<=? and fin_plantation>=?'''
    args=(periode,periode)
    cursor = bdd.get_db().cursor()
    cursor.execute(query,args) 
    data = cursor.fetchall()
    return (month,data)