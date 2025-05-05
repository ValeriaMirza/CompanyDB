from db_utils import get_cursor, close_connection
import sys
sys.stdout.reconfigure(encoding='utf-8')

conn, cursor = get_cursor()

cursor.execute(r"""
    INSERT INTO "FinanceMiIncomeMetrics" (
        period_id,
        net_income_loss_summary_of_business_results,
        net_income_loss_summary_of_business_results_unit_ref,
        ordinary_income_loss_summary_of_business_results,
        ordinary_income_loss_summary_of_business_results_unit_ref,
        ordinary_income_summary_of_business_results,
        ordinary_income_summary_of_business_results_unit_ref
    )
    SELECT 
        fmp.id,
        (management_index_data->> 'net_income_loss_summary_of_business_results')::BIGINT,
        management_index_data->> 'net_income_loss_summary_of_business_results_unit_ref',
        (management_index_data->> 'ordinary_income_loss_summary_of_business_results')::BIGINT,
        management_index_data->> 'ordinary_income_loss_summary_of_business_results_unit_ref',
        (management_index_data->> 'ordinary_income_summary_of_business_results')::BIGINT,
        management_index_data->> 'ordinary_income_summary_of_business_results_unit_ref'
    FROM temp_hojinjoho tj
    JOIN "Company" c ON c.corporate_number = data ->> 'corporate_number'
    JOIN "Finance" f ON f.company_id = c.id
    CROSS JOIN LATERAL jsonb_array_elements(data -> 'finance' -> 'management_index') AS management_index_data
    JOIN "FinanceManagementPeriod" fmp 
        ON fmp.finance_id = f.id AND fmp.period = management_index_data->> 'period'
    WHERE 
        management_index_data->> 'net_income_loss_summary_of_business_results' IS NOT NULL
        OR management_index_data->> 'net_income_loss_summary_of_business_results_unit_ref' IS NOT NULL
        OR management_index_data->> 'ordinary_income_loss_summary_of_business_results' IS NOT NULL
        OR management_index_data->> 'ordinary_income_loss_summary_of_business_results_unit_ref' IS NOT NULL
        OR management_index_data->> 'ordinary_income_summary_of_business_results' IS NOT NULL
        OR management_index_data->> 'ordinary_income_summary_of_business_results_unit_ref' IS NOT NULL
""")

close_connection(conn, cursor)

print("✅ FinanceMiIncomeMetrics data inserted.")
