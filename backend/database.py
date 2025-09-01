import psycopg2
from flask import g

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="ocpdb",
        user="elamraoui",
        password="admin"
)
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(open("schema.sql", "r").read())
    conn.commit()
    cur.close()
    conn.close()
