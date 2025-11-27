import mysql.connector
from flask import g

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=3320,   
        user='root',
        password='',
        database='fley_snow_db'
    )
    return conn


def close_db_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
