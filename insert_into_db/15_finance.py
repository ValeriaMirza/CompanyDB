from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "Finance" (
        company_id,
        accounting_standards,
        fiscal_year_cover_page
    )
    SELECT 
        c.id,
        f_data ->> 'accounting_standards' AS accounting_standards,
        f_data ->> 'fiscal_year_cover_page' AS fiscal_year_cover_page
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    CROSS JOIN LATERAL (
        SELECT tj.data -> 'finance' AS f_data
    ) AS finance
    WHERE 
        f_data ->> 'accounting_standards' IS NOT NULL 
        OR f_data ->> 'fiscal_year_cover_page' IS NOT NULL;
""")

close_connection(conn, cursor)

print("✅ Finance data inserted into Finance table")
