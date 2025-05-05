from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "Procurement" (
        company_id,
        government_departments,
        title,
        amount,
        date_of_order,
        joint_signatures
    )
    SELECT 
        c.id,
        procurement_data->> 'government_departments' AS government_departments,
        procurement_data->> 'title' AS title,
        (procurement_data->> 'amount')::BIGINT AS amount,
        TO_TIMESTAMP(procurement_data->> 'date_of_order', 'YYYY-MM-DD"T"HH24:MI:SS.MS"Z"')::TIMESTAMPTZ AS date_of_order,
        procurement_data->> 'joint_signatures' AS joint_signatures
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    CROSS JOIN LATERAL jsonb_array_elements(tj.data -> 'procurement') AS procurement_data
    WHERE 
        procurement_data ->> 'government_departments' IS NOT NULL;
""")

close_connection(conn, cursor)

print("✅ Procurement records inserted into Procurement")
