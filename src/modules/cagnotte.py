import modules.bdd as bdd
from datetime import datetime

def cagnotte(pseudo,somme):
    date = datetime.now()
    query = '''SELECT id from user WHERE pseudo = ?'''
    arg = [pseudo]
    cursor = bdd.get_db().cursor()
    cursor.execute(query,arg)
    id = cursor.fetchall()[0]
    query2 = '''INSERT INTO transactions (id_user,cagnotte_temp,date) VALUES (?,?,?)'''
    arg2 = [id[0],somme,date]
    db = bdd.get_db()
    cursor2=db.cursor()
    cursor2.execute(query2,arg2)
    db.commit()