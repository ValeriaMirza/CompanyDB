from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "Certification" (
        company_id, 
        title, 
        government_departments,
        category,
        date_of_approval,
        expiration_date,
        enterprise_scale,
        target
    )
    SELECT 
        c.id,
        cert_data->> 'title',
        cert_data->> 'government_departments',
        cert_data->> 'category',
        cert_data->> 'date_of_approval',
        cert_data->> 'expiration_date',
        cert_data->> 'enterprise_scale',
        cert_data->> 'target'
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    CROSS JOIN LATERAL jsonb_array_elements(tj.data -> 'certification') AS cert_data
    WHERE cert_data ->> 'title' IS NOT NULL;
""")

close_connection(conn, cursor)

print("✅ Full certifications inserted into Certification")
