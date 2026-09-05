import mysql.connector
from flask import g,current_app

def open_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host= current_app['MYSQL_HOST'], 
            user= current_app['MYSQL_USER'], 
            password= current_app['MYSQL_PASSWORD'],
            database= current_app['MYSQL_DATABASE']
        )
    return g.db

def close_db(e=None):
    db = g.pop('db',None)
    if db is not None:
        db.close()
