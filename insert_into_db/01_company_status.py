from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute("""
    INSERT INTO "CompanyStatus" (status)
    SELECT DISTINCT data ->> 'status'
    FROM temp_hojinjoho
    WHERE data ->> 'status' IS NOT NULL
""")

close_connection(conn, cursor)

print("Distinct statuses inserted into CompanyStatus")
