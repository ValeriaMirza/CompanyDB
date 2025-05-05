from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "WomenActivityInfo" (
        company_id,
        female_share_of_manager,
        female_share_of_officers,
        female_workers_proportion,
        female_workers_proportion_type,
        gender_total_of_manager,
        gender_total_of_officers
    )
    SELECT 
        c.id AS company_id,
        (tj.data -> 'workplace_info' -> 'women_activity_infos' ->> 'female_share_of_manager')::INT,
        (tj.data -> 'workplace_info' -> 'women_activity_infos' ->> 'female_share_of_officers')::INT,
        (tj.data -> 'workplace_info' -> 'women_activity_infos' ->> 'female_workers_proportion')::FLOAT,
        tj.data -> 'workplace_info' -> 'women_activity_infos' ->> 'female_workers_proportion_type',
        (tj.data -> 'workplace_info' -> 'women_activity_infos' ->> 'gender_total_of_manager')::INT,
        (tj.data -> 'workplace_info' -> 'women_activity_infos' ->> 'gender_total_of_officers')::INT
    FROM temp_hojinjoho tj
    JOIN "Company" c
        ON c.corporate_number = tj.data ->> 'corporate_number'
    WHERE tj.data -> 'workplace_info' -> 'women_activity_infos' IS NOT NULL;
""")

close_connection(conn, cursor)
print("✅ Inserted into WomenActivityInfo")

