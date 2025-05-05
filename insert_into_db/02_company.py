from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute("""
    INSERT INTO "Company" (corporate_number, status_id)
    SELECT 
        data ->> 'corporate_number' AS corporate_number,
        cs.id AS status_id
    FROM temp_hojinjoho th
    LEFT JOIN "CompanyStatus" cs ON cs.status = th.data ->> 'status'
    WHERE data ->> 'corporate_number' IS NOT NULL;
""")

close_connection(conn, cursor)

print("Data with corporate_number and status_id inserted into Company")
