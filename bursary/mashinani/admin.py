from django.contrib import admin
from .models import Bank, Institution, InstitutionAccount, Constituency, VoterRegister, StudentRegister, FinancialYear, BursaryApplication

models_to_register = [Institution, Bank, InstitutionAccount, Constituency, VoterRegister, StudentRegister, FinancialYear, BursaryApplication]

for model in models_to_register:
    admin.site.register(model)
