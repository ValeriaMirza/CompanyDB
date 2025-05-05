from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "Patent" (
        company_id,
        title,
        application_number,
        application_date,
        patent_type,
        code_value,
        code_name,
        japanese_name
    )
    SELECT 
        c.id,
        patent_data->> 'title' AS title,
        patent_data->> 'application_number' AS application_number,
        patent_data->> 'application_date' AS application_date,
        patent_data->> 'patent_type' AS patent_type,
        classification->> 'コード値' AS code_value,
        classification->> 'コード名' AS code_name,
        classification->> '日本語' AS japanese_name
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    CROSS JOIN LATERAL jsonb_array_elements(tj.data -> 'patent') AS patent_data
    LEFT JOIN LATERAL jsonb_array_elements(patent_data -> 'classifications') AS classification
        ON jsonb_typeof(patent_data -> 'classifications') = 'array'
    WHERE 
        patent_data ->> 'title' IS NOT NULL
        AND (classification ->> 'コード値' IS NOT NULL);
""")

close_connection(conn, cursor)

print("✅ Patents with classifications inserted into Patent")
