from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "CompanyIndustry" (company_id, industry_id)
    SELECT 
        c.id AS company_id,
        i.id AS industry_id
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    CROSS JOIN LATERAL jsonb_array_elements_text(tj.data -> 'business_items') AS item_code(code)
    JOIN "Industry" i
        ON i.code = item_code.code
""")

close_connection(conn, cursor)

print("✅ Company-Industry relations inserted into CompanyIndustry table")
