from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')


conn, cursor = get_cursor()

cursor.execute("""
    INSERT INTO "CompanyDates" (company_id, founding_year, date_of_establishment)
    SELECT 
        c.id,
        (data ->> 'founding_year')::integer,
        data ->> 'date_of_establishment'
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = tj.data ->> 'corporate_number'
    WHERE 
        data ->> 'founding_year' IS NOT NULL OR data ->> 'date_of_establishment' IS NOT NULL;
""")

close_connection(conn, cursor)
print("✅ Company dates inserted into CompanyDates")
