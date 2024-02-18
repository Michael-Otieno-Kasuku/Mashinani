from django.db import models

class Bank(models.Model):
    bank_name = models.CharField(max_length=20, primary_key=True, help_text="Enter a valid Bank Name")

    def __str__(self):
        return f"{self.bank_name}"

class Institution(models.Model):
    institution_name = models.CharField(max_length=255, primary_key=True,help_text="Enter a valid Institution Name")

    def __str__(self):
        return f"{self.institution_name}"

class InstitutionAccount(models.Model):
    institution_account_number = models.CharField(max_length=20, primary_key=True help_text="Enter a valid Institution Account Number", blank=True)
    institution_name = models.ForeignKey(Institution, on_delete=models.CASCADE, help_text="Enter a valid Institution Name")
    bank_name = models.ForeignKey(Bank, on_delete=models.CASCADE, help_text="Enter a valid Bank Name")

    def __str__(self):
        return f"{self.institution_account_number self.institution_name self.bank_name}"

class BursaryApplication(models.Model):
    serial_number = models.CharField(max_length=8, primary_key=True, help_text="Auto-generated serial number")
    national_id = models.ForeignKey(VoterRegister, on_delete=models.CASCADE, help_text="Enter a valid National ID Number")
    registration_number = models.ForeignKey(StudentRegister, on_delete=models.CASCADE, help_text="Enter a valid Student Registration Number")
    institution_name = models.ForeignKey(Institution, on_delete=models.CASCADE, help_text="Enter a valid Institution Name")
    institution_account_number = models.ForeignKey(InstitutionAccount, on_delete=models.CASCADE, help_text="Enter a valid Institution Account Number")
    financial_year = models.ForeignKey(FinancialYear, on_delete=models.CASCADE, help_text="Enter a valid Financial Year")
    date_submitted = models.DateTimeField(auto_now_add=True, help_text="Date of submission")
    amount_disbursed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Amount disbursed in Ksh")
    date_disbursed = models.DateTimeField(null=True, blank=True, help_text="Date of disbursement")

    def __str__(self):
        return f"{self.serial_number self.national_id self.registration_number self.institution_name self.institution_account_number self.financial_year self.date_submitted self.amount_disbursed self.date_disbursed}"

class Constituency(models.Model):
    constituency = models.CharField(max_length=255, primary_key=True, help_text="Enter the constituency")

    def __str__(self):
        return f"{self.constituency}"

class VoterRegister(models.Model):
    national_id = models.CharField(max_length=20, primary_key=True, help_text="Enter a valid National ID Number")
    constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE, help_text="Enter the Constituency")

    def __str__(self):
        return f"{self.national_id self.constituency}"

class StudentRegister(models.Model):
    registration_number = models.CharField(max_length=20, primary_key=True, help_text="Enter a valid Student Registration Number")
    national_id = models.ForeignKey(VoterRegister, on_delete=models.CASCADE, help_text="Enter a valid National ID Number")
    institution_name = models.ForeignKey(Institution, on_delete=models.CASCADE, help_text="Enter a Valid Institution")
    first_name = models.CharField(max_length=255, help_text="Enter the first name")
    middle_name = models.CharField(max_length=255, help_text="Enter the middle name")
    last_name = models.CharField(max_length=255, help_text="Enter the last name")

    def __str__(self):
        return f"{self.registration_number self.national_id self.institution_name self.first_name self.middle_name self.last_name}"

class FinancialYear(models.Model):
    financial_year = models.CharField(max_length=20, primary_key=True, help_text="Enter a valid Financial Year")

    def __str__(self):
        return f"{self.financial_year}"
