from django.contrib import admin
from .models import Institution, BursaryApplication, VoterRegistration, StudentRegister

models_to_register = [Institution, BursaryApplication, VoterRegistration, StudentRegister]

for model in models_to_register:
    admin.site.register(model)
