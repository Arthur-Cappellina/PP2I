from flask import session
from passlib.hash import sha256_crypt

def isConnected():
    return len(session) > 0

def get_user_position(): 
    print(session)
    return session["connexion"]["latitude"], session["connexion"]["longitude"]

def inscrire(request):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    email = request.form['email']
    password = sha256_crypt.encrypt(request.form['password'])
    engine = create_engine('sqlite:///db_users.db')
    con = engine.connect()
    statement = text('INSERT INTO log_utilisateur(first_name,last_name,username,email,password) VALUES( :f, :l, :u, :e, :p)')
    con.execute(statement, { 'f': first_name ,'l': last_name ,'u': username ,'e': email ,'p': password })
    con.close()