from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute("""
    INSERT INTO "CompanyClosure" (company_id, close_cause, close_date)
    SELECT 
        c.id,
        data ->> 'close_cause',
        data ->> 'close_date'
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = data ->> 'corporate_number'
    WHERE 
        data ->> 'close_cause' IS NOT NULL OR data ->> 'close_date' IS NOT NULL;
""")

close_connection(conn, cursor)
print("✅ Company closures inserted into CompanyClosure")
