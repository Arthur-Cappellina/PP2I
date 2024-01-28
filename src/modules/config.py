from flask_mail import Mail, Message
from flask import Flask

def setup(app):
    UPLOAD_FOLDER = './static/img'
    app.secret_key = b"6702ffe5d5961ebe3fd3fd13ced7562b33d1db40478d49d3cef58678dbbb8c09"
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'potagix372@gmail.com'
    app.config['MAIL_PASSWORD'] = 'erxyotnvhtfowrne'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    mail = Mail(app)
    return mail