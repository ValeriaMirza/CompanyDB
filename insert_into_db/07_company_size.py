from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "CompanySize" (
        company_id, 
        employee_number, 
        company_size_male, 
        company_size_female, 
        qualification_grade
    )
    SELECT 
        c.id,
        CASE 
            WHEN regexp_replace(data ->> 'employee_number', '[^0-9]', '', 'g') ~ '^\d+$'
            THEN regexp_replace(data ->> 'employee_number', '[^0-9]', '', 'g')::int 
            ELSE NULL 
        END,
        CASE 
            WHEN regexp_replace(data ->> 'company_size_male', '[^0-9]', '', 'g') ~ '^\d+$'
            THEN regexp_replace(data ->> 'company_size_male', '[^0-9]', '', 'g')::int 
            ELSE NULL 
        END,
        CASE 
            WHEN regexp_replace(data ->> 'company_size_female', '[^0-9]', '', 'g') ~ '^\d+$'
            THEN regexp_replace(data ->> 'company_size_female', '[^0-9]', '', 'g')::int 
            ELSE NULL 
        END,
        data ->> 'qualification_grade'
    FROM temp_hojinjoho tj
    JOIN "Company" c
    ON c.corporate_number = data ->> 'corporate_number'
    WHERE 
        (data ->> 'employee_number') IS NOT NULL 
        OR (data ->> 'company_size_male') IS NOT NULL 
        OR (data ->> 'company_size_female') IS NOT NULL 
        OR (data ->> 'qualification_grade') IS NOT NULL;
""")


close_connection(conn, cursor)
print("✅ Company sizes inserted into CompanySize")
