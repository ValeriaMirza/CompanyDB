from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "FinanceManagementPeriod" (
        finance_id, 
        period
    )
        SELECT 
        f.id,
        management_index_data->> 'period' AS period
    FROM temp_hojinjoho tj
    JOIN "Company" c ON c.corporate_number = data ->> 'corporate_number'
    JOIN "Finance" f ON f.company_id = c.id
    CROSS JOIN LATERAL jsonb_array_elements(data -> 'finance' -> 'management_index') AS management_index_data
    WHERE 
        management_index_data->> 'period' IS NOT NULL;

""")

close_connection(conn, cursor)

print("✅ FinanceManagementPeriod data inserted into FinanceManagementPeriod")
