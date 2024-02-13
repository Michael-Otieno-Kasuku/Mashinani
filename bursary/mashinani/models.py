from django.db import models

class Institution(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

class BursaryApplication(models.Model):
    id = models.AutoField(primary_key=True)
    national_id = models.CharField(max_length=20, unique=True, help_text="Enter a valid National ID Number", blank=True)
    registration_number = models.CharField(max_length=20, unique=True, help_text="Enter a valid Student Registration Number", blank=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, help_text="Choose the Tertiary Institution")
    institution_account_number = models.CharField(max_length=20, help_text="Enter a valid Institution Account Number", blank=True)
    financial_year = models.CharField(max_length=10, help_text="Enter the financial year", blank=True)
    serial_number = models.CharField(max_length=8, unique=True, help_text="Auto-generated serial number", blank=True)
    date_submitted = models.DateTimeField(auto_now_add=True, help_text="Date of submission")
    amount_disbursed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Amount disbursed in Ksh")
    date_disbursed = models.DateTimeField(null=True, blank=True, help_text="Date of disbursement")

class VoterRegistration(models.Model):
    national_id = models.CharField(max_length=20, primary_key=True, help_text="Enter a valid National ID Number")
    constituency = models.CharField(max_length=255, help_text="Enter the constituency")

class StudentRegister(models.Model):
    id = models.AutoField(primary_key=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, help_text="Choose the Tertiary Institution")
    registration_number = models.CharField(max_length=20, unique=True, help_text="Enter a valid Student Registration Number")
    student_name = models.CharField(max_length=255, help_text="Enter the student's name")
