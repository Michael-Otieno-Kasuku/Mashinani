from django import forms
from .models import BursaryApplication, Institution, FinancialYear, Ward, Account

class ApplicationForm(forms.ModelForm):
    institution_id = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        required=True,
        label='Institution Name',
        widget=forms.Select(attrs={'class': 'blue-input-box', 'placeholder': 'Select an institution'}),
    )
    financial_year_id = forms.ModelChoiceField(
        queryset=FinancialYear.objects.all(),
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
            'account_number': forms.TextInput(attrs={'class': 'blue-input-box', 'placeholder': 'Enter account number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Correctly set the initial value based on the existing instance
        if self.instance and hasattr(self.instance, 'institution_id') and self.instance.institution_id:
            self.fields['institution_id'].initial = self.instance.institution.institution_id

    