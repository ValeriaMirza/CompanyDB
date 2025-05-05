from db_utils import get_cursor, close_connection
import sys

sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "FinanceMajorShareholder" (
        finance_id, 
        name_major_shareholders, 
        shareholding_ratio
    )
    SELECT 
        f.id AS finance_id,
        shareholder_data->> 'name_major_shareholders' AS name_major_shareholders,
        (shareholder_data->> 'shareholding_ratio')::FLOAT AS shareholding_ratio
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = tj.data ->> 'corporate_number'
    JOIN "Finance" f
    ON f.company_id = c.id
    CROSS JOIN LATERAL jsonb_array_elements(tj.data -> 'finance' -> 'major_shareholders') AS shareholder_data
    WHERE 
        shareholder_data->> 'name_major_shareholders' IS NOT NULL
        AND shareholder_data->> 'shareholding_ratio' IS NOT NULL;
""")

close_connection(conn, cursor)

print("✅ FinanceMajorShareholder data inserted into FinanceMajorShareholder")
