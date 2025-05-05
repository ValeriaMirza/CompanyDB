import subprocess
import os
import sys
import sys
import time
sys.stdout.reconfigure(encoding='utf-8')

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(project_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "companyproject.settings")

def run_python_script(script_path):
    print(f"\n▶ Running {script_path}")
    try:
        subprocess.run(["python", script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {script_path}: {e}")
        sys.exit(1)

def run_django_migrations():
    print("\n▶ Running Django makemigrations and migrate...")
    
    python_exec = sys.executable

    subprocess.run([python_exec, "manage.py", "makemigrations"], check=True)
    subprocess.run([python_exec, "manage.py", "migrate"], check=True)

def main():
    base = "insert_into_db"

    start_time = time.time()

    
    run_python_script(f"{base}/a_create_database.py")


    run_django_migrations()

    run_python_script(f"{base}/b_get_zip.py")
    run_python_script(f"{base}/c_unzip.py")
    run_python_script(f"{base}/d_convert_to_ndjson.py")
    run_python_script(f"{base}/e_ndjson_to_temp_table.py")

    run_python_script(f"{base}/00_get_industry.py")
    run_python_script(f"{base}/01_company_status.py")
    run_python_script(f"{base}/02_company.py")
    run_python_script(f"{base}/03_company_names.py")
    run_python_script(f"{base}/04_company_location.py")
    run_python_script(f"{base}/05_company_closure.py")
    run_python_script(f"{base}/06_company_dates.py")
    run_python_script(f"{base}/07_company_size.py")
    run_python_script(f"{base}/08_company_contact.py")
    run_python_script(f"{base}/09_company_financial_summary.py")
    run_python_script(f"{base}/10_certification.py")
    run_python_script(f"{base}/11_commendation.py")
    run_python_script(f"{base}/12_patent.py")
    run_python_script(f"{base}/13_procurement.py")
    run_python_script(f"{base}/14_subsidy.py")
    run_python_script(f"{base}/15_finance.py")
    run_python_script(f"{base}/16_company_industry.py")
    run_python_script(f"{base}/17_workplace_base_info.py")
    run_python_script(f"{base}/18_childcare_compatibility.py")
    run_python_script(f"{base}/19_women_activity_info.py")
    run_python_script(f"{base}/20_fin_major_shareholder.py")
    run_python_script(f"{base}/21_fin_management_period.py")
    run_python_script(f"{base}/22_fin_mi_asset_metrics.py")
    run_python_script(f"{base}/23_fin_mi_capital_metrics.py")
    run_python_script(f"{base}/24_-fin_mi_income_metrics.py")
    run_python_script(f"{base}/25_fin_mi_employee_metrics.py")
    run_python_script(f"{base}/26_fin_mi_revenue_metrics.py")


    end_time = time.time()
    total_time = end_time - start_time
    print(f"\n✅ All steps completed successfully in {total_time:.2f} seconds.")

if __name__ == "__main__":
    main()
