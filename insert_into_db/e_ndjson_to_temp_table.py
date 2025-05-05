
import os
import psycopg2
import sys
from db_utils import get_cursor, close_connection


sys.stdout.reconfigure(encoding='utf-8')


ndjson_dir = 'hojinjoho_ndjson'

def main():
    conn, cur = get_cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS temp_hojinjoho (
            id   SERIAL PRIMARY KEY,
            data JSONB NOT NULL
        );
    """)
    conn.commit()

    for fname in os.listdir(ndjson_dir):
        if not fname.lower().endswith('.ndjson'):
            continue
        path = os.path.join(ndjson_dir, fname)
        with open(path, 'r', encoding='utf-8', newline='\n') as f:
            sql = """
                COPY temp_hojinjoho(data)
                FROM STDIN
                WITH (FORMAT text, ENCODING 'UTF8');
            """
            cur.copy_expert(sql, f)
            conn.commit()
            print(f"[✔] Loaded {fname} ({sum(1 for _ in open(path, 'r', encoding='utf-8'))} rows)")

    close_connection(conn, cur)

if __name__ == '__main__':
    main()
