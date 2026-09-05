import mysql.connector             # --> db specific connector api
from flask import g,current_app    # --> g is temporary storage for a request and current_app is reference of Flask object (app)


def open_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host= current_app.config['MYSQL_HOST'], 
            user= current_app.config['MYSQL_USER'], 
            password= current_app.config['MYSQL_PASSWORD'],
            database= current_app.config['MYSQL_DATABASE']
        )
    return g.db

def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()
