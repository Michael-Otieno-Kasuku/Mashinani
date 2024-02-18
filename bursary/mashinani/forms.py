from django import forms
from .models import BursaryApplication, Institution

class ApplicationForm(forms.ModelForm):
    institution_name = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        required=True,
        label='Institution Name',
        widget=forms.Select(attrs={'class': 'blue-input-box'}),
    )
    financial_year = forms.ModelChoiceField(
        queryset=FinancialYear.objects.all(),
        required=True,
        label='Financial Year',
        widget=forms.Select(attrs={'class': 'blue-input-box'}),
    )

    class Meta:
        model = BursaryApplication
        fields = ['national_id', 'registration_number', 'institution_name', 'institution_account_number', 'financial_year']
        labels = {
            'national_id': 'National ID Number',
            'registration_number': 'Student Registration Number',
            'institution_name': 'Institution',
            'institution_account_number': 'Institution Account Number',
            'financial_year': 'Financial Year',
        }
        widgets = {
            'national_id': forms.TextInput(attrs={'class': 'blue-input-box'}),
            'registration_number': forms.TextInput(attrs={'class': 'blue-input-box'}),
            'institution_account_number': forms.TextInput(attrs={'class': 'blue-input-box'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Correctly set the initial value based on the existing instance
        if self.instance and hasattr(self.instance, 'institution') and self.instance.institution_name:
            self.fields['institution_name'].initial = self.instance.institution.institution_name
        
        if self.instance and hasattr(self.instance, 'financial_year' and self.instance.financial_year):
            self.fields['financial_year'].initial = self.instance.financial_year.financial_year

class ProgressTrackingForm(forms.Form):
    serial_number = forms.CharField(
        max_length=8,
        help_text="Enter the 8-alphanumeric serial number",
        widget=forms.TextInput(attrs={'class': 'blue-input-box'})
    )
