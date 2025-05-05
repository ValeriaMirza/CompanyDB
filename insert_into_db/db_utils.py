import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn_info = {
    'dbname':   'corporate_db',
    'user':     'postgres',
    'password': 'postgres',
    'host':     'db',  # or 'localhost' if outside Docker
    'port':     5432
}

def get_cursor():
    conn = psycopg2.connect(
        host=conn_info['host'],
        database=conn_info['dbname'],
        user=conn_info['user'],
        password=conn_info['password'],
        port=conn_info['port']
    )
    return conn, conn.cursor()

def close_connection(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()

def get_admin_cursor():
    conn = psycopg2.connect(
        dbname='postgres',
        user=conn_info['user'],
        password=conn_info['password'],
        host=conn_info['host'],
        port=conn_info['port']
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn, conn.cursor()

def get_conn_info():
    return conn_info
