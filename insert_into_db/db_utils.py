import psycopg2

def get_cursor():
    conn = psycopg2.connect(
        host="localhost",
        database="corporate_db",
        user="postgres",
        password="postgres"
    )
    return conn, conn.cursor()

def close_connection(conn, cursor):
    conn.commit()
    cursor.close()
    conn.close()
