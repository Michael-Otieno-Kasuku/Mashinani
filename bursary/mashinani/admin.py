from django.contrib import admin
from .models import Bank, Institution, Account,County, Constituency, Ward, Student, FinancialYear,Resident, BursaryApplication

models_to_register = [Institution, Bank, Account, County,Constituency, Ward, Student, FinancialYear, Resident,BursaryApplication]

for model in models_to_register:
    admin.site.register(model)
