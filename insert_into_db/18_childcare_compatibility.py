from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "ChildcareCompatibility" (
        company_id,
        maternity_leave_acquisition_num,
        number_of_maternity_leave,
        number_of_paternity_leave,
        paternity_leave_acquisition_num
    )
    SELECT 
        c.id AS company_id,
        (tj.data -> 'workplace_info' -> 'compatibility_of_childcare_and_work' ->> 'maternity_leave_acquisition_num')::INT,
        (tj.data -> 'workplace_info' -> 'compatibility_of_childcare_and_work' ->> 'number_of_maternity_leave')::INT,
        (tj.data -> 'workplace_info' -> 'compatibility_of_childcare_and_work' ->> 'number_of_paternity_leave')::INT,
        (tj.data -> 'workplace_info' -> 'compatibility_of_childcare_and_work' ->> 'paternity_leave_acquisition_num')::INT
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    WHERE tj.data -> 'workplace_info' -> 'compatibility_of_childcare_and_work' IS NOT NULL;
""")


close_connection(conn, cursor)

print("✅ Inserted into ChildcareCompatibility")

