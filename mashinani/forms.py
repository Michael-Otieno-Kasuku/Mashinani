from django import forms
from django.contrib.auth.hashers import make_password
from .models import Bank, Institution, Account,Country, Region, County, Constituency, Ward, Student, FinancialYear,Resident, BursaryApplication, User

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Reenter your password', 'class': 'form-control', 'id': 'confirm_password'})
    )

    class Meta:
        model = User
        fields = ['national_id_no', 'email_address', 'password_hash']
        labels = {
            'national_id_no': 'National ID Number',
            'email_address': 'Email Address',
            'password_hash': 'Password',
            'confirm_password': 'Confirm Password',
        }
        widgets = {
            'national_id_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your national id number'}),
            'email_address': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'password_hash': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password_hash")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Password and confirm password do not match!")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data["password_hash"])
        if commit:
            instance.save()
        return instance

class LoginForm(forms.Form):
    email_address = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email_address = cleaned_data.get("email_address")
        password = cleaned_data.get("password")
        return cleaned_data

class PasswordResetForm(forms.Form):
    email_address = forms.EmailField(
        label='Email Address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'})
    )

    def clean_email_address(self):
        email = self.cleaned_data.get('email_address')
        if not User.objects.filter(email_address=email).exists():
            raise forms.ValidationError("This email address is not associated with any account!")
        return email

class ApplicationForm(forms.ModelForm):
    institution_id = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        required=True,
        label='Institution Name',
        widget=forms.Select(attrs={'class': 'blue-input-box', 'placeholder': 'Select an institution'}),
    )
    financial_year_id = forms.ModelChoiceField(
        queryset=FinancialYear.objects.filter(financial_year_status='Open'),  # Filter for 'Open' financial years
        required=True,
        label='Financial Year',
        widget=forms.Select(attrs={'class': 'blue-input-box', 'placeholder': 'Select a financial year'}),
    )
    ward_id = forms.ModelChoiceField(
        queryset=Ward.objects.all(),
        required=True,
        label='Current Ward of Residence',
        widget=forms.Select(attrs={'class': 'blue-input-box', 'placeholder': 'Select a ward'}),
    )

    class Meta:
        model = BursaryApplication
        fields = ['national_id_no', 'registration_number', 'institution_id', 'account_number', 'ward_id', 'financial_year_id']
        labels = {
            'national_id_no': 'National ID Number',
            'registration_number': 'Student Registration Number',
            'institution_id': 'Institution Name',
            'account_number': 'Institution Account Number',
            'ward_id': 'Current Ward of Residence',
            'financial_year_id': 'Financial Year',
        }
        widgets = {
            'national_id_no': forms.TextInput(attrs={'class': 'blue-input-box', 'placeholder': 'Enter national ID number'}),
            'registration_number': forms.TextInput(attrs={'class': 'blue-input-box', 'placeholder': 'Enter registration number'}),
            'account_number': forms.TextInput(attrs={'class': 'blue-input-box', 'placeholder': 'Enter institution account number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Correctly set the initial value based on the existing instance
        if self.instance and hasattr(self.instance, 'institution_id') and self.instance.institution_id:
            self.fields['institution_id'].initial = self.instance.institution.institution_id
