from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute("""
    INSERT INTO "CompanyName" (company_id, name, name_en, kana)
    SELECT 
        c.id,
        data ->> 'name',
        data ->> 'name_en',
        data ->> 'kana'
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = tj.data ->> 'corporate_number'
    WHERE 
        data ->> 'name' IS NOT NULL OR data ->> 'name_en' IS NOT NULL OR data ->> 'kana' IS NOT NULL;
""")

close_connection(conn, cursor)

print("Company names inserted into CompanyName")
