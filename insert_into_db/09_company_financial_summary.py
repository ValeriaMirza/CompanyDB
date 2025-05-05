from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "CompanyFinancialSummary" (
        company_id, 
        business_summary, 
        capital_stock
    )
    SELECT 
        c.id,
        data ->> 'business_summary',
        CASE 
            WHEN regexp_replace(data ->> 'capital_stock', '[^0-9]', '', 'g') ~ '^\d+$'
            THEN regexp_replace(data ->> 'capital_stock', '[^0-9]', '', 'g')::NUMERIC 
            ELSE NULL 
        END
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = data ->> 'corporate_number'
    WHERE 
        (data ->> 'business_summary') IS NOT NULL
        OR (data ->> 'capital_stock') IS NOT NULL;
""")

close_connection(conn, cursor)

print("✅ Company financial summaries inserted into CompanyFinancialSummary")
