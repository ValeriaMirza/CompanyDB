from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "Subsidy" (
        company_id,
        government_departments,
        title,
        amount,
        date_of_approval,
        subsidy_resource,
        note,
        target,
        joint_signatures
    )
    SELECT 
        c.id,
        subsidy_data->> 'government_departments' AS government_departments,
        subsidy_data->> 'title' AS title,
        subsidy_data->> 'amount' AS amount,
        subsidy_data->> 'date_of_approval' AS date_of_approval,
        subsidy_data->> 'subsidy_resource' AS subsidy_resource,
        subsidy_data->> 'note' AS note,
        subsidy_data->> 'target' AS target,
        subsidy_data->> 'joint_signatures' AS joint_signatures
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = data ->> 'corporate_number'
    CROSS JOIN LATERAL jsonb_array_elements(data -> 'subsidy') AS subsidy_data
    WHERE 
        subsidy_data ->> 'title' IS NOT NULL;
""")

close_connection(conn, cursor)

print("✅ Subsidy records inserted into Subsidy")
