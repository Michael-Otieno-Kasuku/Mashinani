import re
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import RegexValidator,MinValueValidator, MaxValueValidator

#Most of the data will be inserted into the database using migrations during deployment after they have been gathered from different sources

"""
When we will be launching this system we will request for the following documents from the users:

1. A copy of national id card
2. A copy of birth certificate
3. A copy of admission letter
4. A copy of fee structure

Then we will extract data from this documents and populate into our database models via admin site or using migrations

This will only happen once for new users
"""
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
    account_number = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid Institution Account Number",
        validators=[RegexValidator(
            regex=r'^\d{14}$',  # Regex for 14 digits
            message='Account number must be 14 digits long!',
            code='invalid_account_number'
        )]
    )

    def __str__(self):
        return self.account_number

class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=255, unique=True, help_text="Enter a valid Country name")

    def __str__(self):
        return self.country_name

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    region_name = models.CharField(max_length=255, unique=True, help_text="Enter the Region name")

    def __str__(self):
        return self.region_name

class County(models.Model):
    county_id = models.AutoField(primary_key=True)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    county_name = models.CharField(max_length=255, unique=True, help_text="Enter the county name")

    def __str__(self):
        return self.county_name

class Constituency(models.Model):
    constituency_id = models.AutoField(primary_key=True)
    county_id = models.ForeignKey(County, on_delete=models.CASCADE)
    constituency_name = models.CharField(max_length=255, unique=True, help_text="Enter the constituency name")

    def __str__(self):
        return self.constituency_name

class Ward(models.Model):
    ward_id = models.AutoField(primary_key=True)
    constituency_id = models.ForeignKey(Constituency, on_delete=models.CASCADE)
    ward_name = models.CharField(max_length=200, unique=True, help_text="Enter the ward name")

    def __str__(self):
        return self.ward_name

class Resident(models.Model):
    resident_id = models.AutoField(primary_key=True)
    national_id_no = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid National ID Number",
        validators=[RegexValidator(
            regex=r'^\d{8}$',  # Regex for 8 digits
            message='National ID number must be 8 digits long!',
            code='invalid_national_id_number'
        )]
    )
    ward_id = models.ForeignKey(Ward, on_delete=models.CASCADE)

    def __str__(self):
        return self.national_id_no

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    national_id_no = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid National ID Number",
        validators=[RegexValidator(
            regex=r'^\d{8}$',  # Regex for 8 digits
            message='National ID number must be 8 digits long!',
            code='invalid_national_id_number'
        )]
    )
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    registration_number = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid Student Registration Number",
        validators=[RegexValidator(
            regex=r'^(COM|SIT|SIK|ETS|DIT|EDS|EDA)/[A-Z]/\d{2}-\d{5}/\d{4}$',  # Regex for specified format
            message='Registration number must be in the format "COM/B/01-00162/2021".',
            code='invalid_registration_number'
        )]
    )
    first_name = models.CharField(max_length=255, help_text="Enter the first name")
    last_name = models.CharField(max_length=255, help_text="Enter the last name")

    def __str__(self):
        return self.registration_number

def validate_financial_year(value):
    parts = value.split('/')
    if len(parts) != 2:
        raise ValidationError('Invalid financial year!')

    AAAA, BBBB = parts[0], parts[1]
    if not (AAAA.isdigit() and BBBB.isdigit()):
        raise ValidationError('Invalid financial year!')

    AAAA, BBBB = int(AAAA), int(BBBB)
    if not (1900 <= AAAA <= 2100 and 1900 <= BBBB <= 2100 and AAAA == BBBB - 1):
        raise ValidationError('Invalid financial year!')

def validate_financial_year_status(value):
    if value not in ['Open', 'Closed']:
        raise ValidationError('Financial year status should be either "Open" or "Closed"!')

class FinancialYear(models.Model):
    financial_year_id = models.AutoField(primary_key=True)
    financial_year = models.CharField(
        max_length=9,  # Length of AAAA/BBBB
        unique=True,
        help_text="Enter a valid Financial Year (e.g., 2021/2022)",
        validators=[validate_financial_year]
    )
    FINANCIAL_YEAR_STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    financial_year_status = models.CharField(
        max_length=6,
        choices=FINANCIAL_YEAR_STATUS_CHOICES,
        help_text="Enter a valid financial year status",
        validators=[validate_financial_year_status]
    )

    def __str__(self):
        return self.financial_year

def validate_serial_number(value):
    if not re.match(r'^[a-zA-Z0-9]{10}$', value):
        raise ValidationError('Serial number must be exactly 10 alphanumeric characters!')

class BursaryApplication(models.Model):
    bursary_application_id = models.AutoField(primary_key=True)
    national_id_no = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid National ID Number",
        validators=[RegexValidator(
            regex=r'^\d{8}$',  # Regex for 8 digits
            message='National ID number must be 8 digits long!',
            code='invalid_national_id_number'
        )]
    )
    registration_number = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid Student Registration Number",
        validators=[RegexValidator(
            regex=r'^(COM|SIT|SIK|ETS|DIT|EDS|EDA)/[A-Z]/\d{2}-\d{5}/\d{4}$',  # Regex for specified format
            message='Registration number must be in the format "COM/B/01-00162/2021"!',
            code='invalid_registration_number'
        )]
    )
    institution_id = models.ForeignKey(Institution, on_delete=models.CASCADE)
    account_number = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid Institution Account Number",
        validators=[RegexValidator(
            regex=r'^\d{14}$',  # Regex for 14 digits
            message='Account number must be 14 digits long!',
            code='invalid_account_number'
        )]
    )
    ward_id = models.ForeignKey(Ward, on_delete=models.CASCADE)
    financial_year_id = models.ForeignKey(FinancialYear, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=200, unique=True, help_text="Auto-generated serial number", validators=[validate_serial_number])
    date_submitted = models.DateTimeField(auto_now_add=True, help_text="Date of submission")
    amount_disbursed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Amount disbursed in Ksh",
        validators=[MinValueValidator(0), MaxValueValidator(12000)]
    )
    date_disbursed = models.DateTimeField(null=True, blank=True, help_text="Date of disbursement")

    def clean(self):
        super().clean()
        if self.date_disbursed and self.date_disbursed < self.date_submitted:
            raise ValidationError("Date disbursed should be greater than or equal to the date submitted!")

    def __str__(self):
        return self.serial_number

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    national_id_no = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a valid National ID Number",
        validators=[RegexValidator(
            regex=r'^\d{8}$',  # Regex for 8 digits
            message='National ID number must be 8 digits long!',
            code='invalid_national_id_number'
        )]
    )
    email_address = models.EmailField(max_length=200, unique=True, help_text="Enter a valid email address")
    password_hash = models.CharField(max_length=128, help_text="Enter a valid password")  # Store hashed password

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def clean(self):
        # Custom validation for password field
        if len(self.password_hash) < 8:
            raise ValidationError("Password must be at least 8 characters long!")

    def __str__(self):
        return self.email_address

class PasswordResetToken(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=32)
    expiry_timestamp = models.DateTimeField()
