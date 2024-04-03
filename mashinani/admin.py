from django.contrib import admin
from .models import Bank, Institution, Account,Country, Region, County, Constituency, Ward, Student, FinancialYear,Resident, BursaryApplication, User

models_to_register = [Bank, Institution, Account,Country, Region, County, Constituency, Ward, Student, FinancialYear,Resident, BursaryApplication, User]

for model in models_to_register:
    admin.site.register(model)