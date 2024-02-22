from django.contrib import admin
from .models import Bank, Institution, Account, Constituency, Voter, Student, FinancialYear, BursaryApplication

models_to_register = [Institution, Bank, Account, Constituency, Voter, Student, FinancialYear, BursaryApplication]

for model in models_to_register:
    admin.site.register(model)
