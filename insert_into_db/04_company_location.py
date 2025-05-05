from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute("""
    INSERT INTO "CompanyLocation" (company_id, location, postal_code, company_url)
    SELECT 
        c.id,
        data ->> 'location',
        data ->> 'postal_code',
        data ->> 'company_url'
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = data ->> 'corporate_number'
    WHERE 
        data ->> 'location' IS NOT NULL OR data ->> 'postal_code' IS NOT NULL OR data ->> 'company_url' IS NOT NULL;
""")

close_connection(conn, cursor)
print("✅ Company locations inserted into CompanyLocation")
