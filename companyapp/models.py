from django.db import models

class Company(models.Model):
    corporate_number = models.CharField(max_length=255)
    status = models.ForeignKey('CompanyStatus', on_delete=models.SET_NULL, null=True, blank=True, related_name='companies')

    class Meta:
        db_table = 'Company'

class CompanyName(models.Model):
    company = models.OneToOneField(Company, related_name='name', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    kana = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'CompanyName'


class Industry(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    class Meta:
        db_table = 'Industry'
    

class CompanyIndustry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    class Meta:
        db_table = 'CompanyIndustry'

class CompanyStatus(models.Model):
    status = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'CompanyStatus'

class CompanyDates(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='company_dates')
    founding_year = models.IntegerField(null=True, blank=True)
    date_of_establishment = models.CharField(max_length=255, null=True, blank=True)
    update_date = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'CompanyDates'

class CompanyClosure(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='closure')
    close_cause = models.CharField(max_length=255, null=True, blank=True)
    close_date = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'CompanyClosure'

class CompanyLocation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='locations')
    location = models.CharField(max_length=255, null=True, blank=True)
    postal_code = models.CharField(max_length=255, null=True, blank=True)
    company_url = models.URLField(null=True, blank=True)
    class Meta:
        db_table = 'CompanyLocation'

class CompanyContact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    representative_name = models.CharField(max_length=255, null=True, blank=True)
    representative_position = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'CompanyContact'

class CompanySize(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sizes')
    employee_number = models.IntegerField(null=True, blank=True)
    company_size_male = models.IntegerField(null=True, blank=True)
    company_size_female = models.IntegerField(null=True, blank=True)
    qualification_grade = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'CompanySize'

class CompanyFinancialSummary(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financial_summaries')
    business_summary = models.TextField(null=True, blank=True)
    capital_stock = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = 'CompanyFinancialSummary'


class Certification(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True, blank=True)#can have the same title
    government_departments = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    date_of_approval = models.CharField(max_length=255, null=True, blank=True)
    expiration_date = models.CharField(max_length=255, null=True, blank=True)
    enterprise_scale = models.CharField(max_length=255, null=True, blank=True)
    target = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'Certification'

class Commendation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)#can have the same title
    government_departments = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=1000, null=True, blank=True)
    date_of_commendation = models.CharField(max_length=1000, null=True, blank=True)
    target = models.CharField(max_length=1000, null=True, blank=True)
    class Meta:
        db_table = 'Commendation'

class Finance(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE) 
    accounting_standards = models.CharField(max_length=255, null=True, blank=True)
    fiscal_year_cover_page = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'Finance'

class FinanceMajorShareholder(models.Model):
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE)
    name_major_shareholders = models.CharField(max_length=255, null=True, blank=True)
    shareholding_ratio = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'FinanceMajorShareholder'

class FinanceManagementPeriod(models.Model):
    finance = models.ForeignKey(Finance, on_delete=models.CASCADE)
    period = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'FinanceManagementPeriod'

class FinanceMiAssetMetrics(models.Model):
    period = models.OneToOneField(FinanceManagementPeriod, on_delete=models.CASCADE, primary_key=True)
    net_assets_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    net_assets_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    total_assets_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    total_assets_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        db_table = 'FinanceMiAssetMetrics'

class FinanceMiRevenueMetrics(models.Model):
    period = models.OneToOneField(FinanceManagementPeriod, on_delete=models.CASCADE, primary_key=True)
    
    gross_operating_revenue_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    gross_operating_revenue_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    net_sales_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    net_sales_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    net_premiums_written_summary_of_business_results_ins = models.BigIntegerField(null=True, blank=True)
    net_premiums_written_summary_of_business_results_ins_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    operating_revenue1_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    operating_revenue1_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    operating_revenue2_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    operating_revenue2_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'FinanceMiRevenueMetrics'



class FinanceMiCapitalMetrics(models.Model):
    period = models.OneToOneField(FinanceManagementPeriod, on_delete=models.CASCADE, primary_key=True)
    
    capital_stock_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    capital_stock_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
        db_table = 'FinanceMiCapitalMetrics'

class FinanceMiIncomeMetrics(models.Model):
    period = models.OneToOneField(FinanceManagementPeriod, on_delete=models.CASCADE, primary_key=True)
    net_income_loss_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    net_income_loss_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    ordinary_income_loss_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    ordinary_income_loss_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    ordinary_income_summary_of_business_results = models.BigIntegerField(null=True, blank=True)
    ordinary_income_summary_of_business_results_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        db_table = 'FinanceMiIncomeMetrics'

class FinanceMiEmployeeMetrics(models.Model):
    period = models.OneToOneField(FinanceManagementPeriod, on_delete=models.CASCADE, primary_key=True)
    number_of_employees = models.BigIntegerField(null=True, blank=True)
    number_of_employees_unit_ref = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        db_table = 'FinanceMiEmployeeMetrics'

class Patent(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    application_number = models.CharField(max_length=500, null=True, blank=True)
    application_date = models.CharField(max_length=255, null=True, blank=True)
    patent_type = models.CharField(max_length=255, null=True, blank=True)
    code_value = models.CharField(max_length=255, null=True, blank=True)
    code_name = models.CharField(max_length=255, null=True, blank=True)
    japanese_name = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        db_table = 'Patent'

class Procurement(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    government_departments = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000, null=True, blank=True) 
    amount = models.BigIntegerField(null=True, blank=True) 
    date_of_order = models.DateTimeField(null=True, blank=True)  
    joint_signatures = models.CharField(max_length=1000, null=True, blank=True) 

    class Meta:
        db_table = 'Procurement'



class Subsidy(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    government_departments = models.TextField(null=True, blank=True)
    title = models.TextField(null=True, blank=True) #can have the same title
    amount = models.TextField(null=True, blank=True)
    date_of_approval = models.TextField(null=True, blank=True)
    subsidy_resource = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    target = models.TextField(null=True, blank=True)
    joint_signatures = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'Subsidy'

class WorkplaceBaseInfo(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    average_age = models.FloatField(null=True, blank=True)
    average_continuous_service_years = models.FloatField(null=True, blank=True)
    average_continuous_service_years_type = models.CharField(max_length=255, null=True, blank=True)
    month_average_predetermined_overtime_hours = models.FloatField(null=True, blank=True)
    average_continuous_service_years_female = models.FloatField(null=True, blank=True)
    average_continuous_service_years_male = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = 'WorkplaceBaseInfo'

class ChildcareCompatibility(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    maternity_leave_acquisition_num = models.IntegerField(null=True, blank=True)
    number_of_maternity_leave = models.IntegerField(null=True, blank=True)
    number_of_paternity_leave = models.IntegerField(null=True, blank=True)
    paternity_leave_acquisition_num = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'ChildcareCompatibility'

class WomenActivityInfo(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    female_share_of_manager = models.IntegerField(null=True, blank=True)
    female_share_of_officers = models.IntegerField(null=True, blank=True)
    female_workers_proportion = models.FloatField(null=True, blank=True)
    female_workers_proportion_type = models.CharField(max_length=255,null=True, blank=True)
    gender_total_of_manager = models.IntegerField(null=True, blank=True)
    gender_total_of_officers = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'WomenActivityInfo'

