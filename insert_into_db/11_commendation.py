from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "Commendation" (
        company_id, 
        title, 
        government_departments,
        category, 
        date_of_commendation, 
        target
    )
    SELECT 
        c.id,
        commendation_data->> 'title' AS title,
        commendation_data->> 'government_departments' AS government_departments,
        commendation_data->> 'category' AS category,
        commendation_data->> 'date_of_commendation' AS date_of_commendation,
        commendation_data->> 'target' AS target
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = data ->> 'corporate_number'
    CROSS JOIN LATERAL jsonb_array_elements(data -> 'commendation') AS commendation_data
    WHERE 
        commendation_data ->> 'title' IS NOT NULL;
""")

close_connection(conn, cursor)

print("✅ Commendations inserted into Commendation")
