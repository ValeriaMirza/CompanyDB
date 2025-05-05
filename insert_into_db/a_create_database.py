import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn_info = {
    'dbname':   'corporate_db',
    'user':     'postgres',
    'password': 'postgres',
    'host':     'localhost',
    'port':     5432
}

admin_conn = psycopg2.connect(
    dbname='postgres',
    user=conn_info['user'],
    password=conn_info['password'],
    host=conn_info['host'],
    port=conn_info['port']
)

admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = admin_conn.cursor()

cursor.execute(f"SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{conn_info['dbname']}' AND pid <> pg_backend_pid();")
cursor.execute(f"DROP DATABASE IF EXISTS {conn_info['dbname']};")

cursor.execute(f"CREATE DATABASE {conn_info['dbname']};")

cursor.close()
admin_conn.close()

print(f"Database '{conn_info['dbname']}' has been created.")
