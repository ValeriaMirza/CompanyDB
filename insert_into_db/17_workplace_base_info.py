from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "WorkplaceBaseInfo" (
        company_id,
        average_age,
        average_continuous_service_years,
        average_continuous_service_years_type,
        month_average_predetermined_overtime_hours,
        average_continuous_service_years_female,
        average_continuous_service_years_male
    )
    SELECT 
        c.id AS company_id,
        (tj.data -> 'workplace_info' -> 'base_infos' ->> 'average_age')::FLOAT,
        (tj.data -> 'workplace_info' -> 'base_infos' ->> 'average_continuous_service_years')::FLOAT,
        tj.data -> 'workplace_info' -> 'base_infos' ->> 'average_continuous_service_years_type',
        (tj.data -> 'workplace_info' -> 'base_infos' ->> 'month_average_predetermined_overtime_hours')::FLOAT,
        (tj.data -> 'workplace_info' -> 'base_infos' ->> 'average_continuous_service_years_female')::FLOAT,
        (tj.data -> 'workplace_info' -> 'base_infos' ->> 'average_continuous_service_years_male')::FLOAT
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    WHERE tj.data -> 'workplace_info' -> 'base_infos' IS NOT NULL;
""")



close_connection(conn, cursor)
print("✅ Inserted into WorkplaceBaseInfo")
