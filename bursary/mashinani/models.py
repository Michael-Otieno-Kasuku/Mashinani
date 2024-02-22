from django.db import models

class Bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_name = models.CharField(max_length=200, unique=True, help_text="Enter a valid Bank Name")

    def __str__(self):
        return self.bank_name

class Institution(models.Model):
    institution_id = models.AutoField(primary_key=True)
    institution_name = models.CharField(max_length=255, unique=True,help_text="Enter a valid Institution Name")

    def __str__(self):
        return self.institution_name

class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=200, unique=True, help_text="Enter a valid Account Number")

    def __str__(self):
        return self.account_number

class Constituency(models.Model):
    constituency_id = models.AutoField(primary_key=True)
    constituency_name = models.CharField(max_length=255, unique=True, help_text="Enter the constituency name")

    def __str__(self):
        return self.constituency_name

class Voter(models.Model):
    voter_id = models.AutoField(primary_key=True)
    constituency_id = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    national_id_no = models.CharField(max_length=200, unique=True, help_text="Enter a valid National ID Number")

    def __str__(self):
        return self.national_id_no

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    voter_id = models.ForeignKey(VoterRegister, on_delete=models.CASCADE)
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=200, unique=True, help_text="Enter a valid Student Registration Number")
    first_name = models.CharField(max_length=255, help_text="Enter the first name")
    last_name = models.CharField(max_length=255, help_text="Enter the last name")

    def __str__(self):
        return self.registration_number

class FinancialYear(models.Model):
    financial_year_id = models.AutoField(primary_key=True)
    financial_year = models.CharField(max_length=200, unique=True, help_text="Enter a valid Financial Year")

    def __str__(self):
        return self.financial_year

class BursaryApplication(models.Model):
    bursary_application_id = models.AutoField(primary_key=True)
    voter_id = models.ForeignKey(Voter, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    constituency_id = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    financial_year_id = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=200, unique=True, help_text="Auto-generated serial number")
    date_submitted = models.DateTimeField(auto_now_add=True, help_text="Date of submission")
    amount_disbursed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Amount disbursed in Ksh")
    date_disbursed = models.DateTimeField(null=True, blank=True, help_text="Date of disbursement")

    def __str__(self):
        return self.serial_number
