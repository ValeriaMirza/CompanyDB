from db_utils import get_admin_cursor, get_conn_info

conn_info = get_conn_info()
admin_conn, cursor = get_admin_cursor()

# Terminate existing connections to the DB
cursor.execute(f"""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '{conn_info['dbname']}'
    AND pid <> pg_backend_pid();
""")

# Drop and recreate the database
cursor.execute(f"DROP DATABASE IF EXISTS {conn_info['dbname']};")
cursor.execute(f"CREATE DATABASE {conn_info['dbname']};")

cursor.close()
admin_conn.close()

print(f"✅ Database '{conn_info['dbname']}' has been created.")
