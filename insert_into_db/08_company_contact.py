from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute("""
    INSERT INTO "CompanyContact" (company_id, representative_name, representative_position)
    SELECT 
        c.id,
        data ->> 'representative_name',
        data ->> 'representative_position'
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = data ->> 'corporate_number'
    WHERE 
        data ->> 'representative_name' IS NOT NULL OR data ->> 'representative_position' IS NOT NULL;
""")

close_connection(conn, cursor)
print("✅ Company contacts inserted into CompanyContact")
