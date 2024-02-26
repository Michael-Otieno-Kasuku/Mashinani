from django import forms
from .models import BursaryApplication, Institution, FinancialYear, Constituency, Account

class ApplicationForm(forms.ModelForm):
    institution_id = forms.ModelChoiceField(
        queryset=Institution.objects.all(),
        required=True,
        label='Institution Name',
        widget=forms.Select(attrs={'class': 'blue-input-box'}),
    )
    financial_year_id = forms.ModelChoiceField(
        queryset=FinancialYear.objects.all(),
        required=True,
        label='Financial Year',
        widget=forms.Select(attrs={'class': 'blue-input-box'}),
    )
    constituency_id = forms.ModelChoiceField(
        queryset=Constituency.objects.all(),
        required=True,
        label='Constituency',
        widget=forms.Select(attrs={'class': 'blue-input-box'}),
    )

    class Meta:
        model = BursaryApplication
        fields = ['national_id_no', 'registration_number', 'institution_id', 'account_number', 'constituency_id', 'financial_year_id']
        labels = {
            'national_id_no': 'National ID Number',
            'registration_number': 'Student Registration Number',
            'institution_id': 'Institution Name',
            'account_number': 'Institution Account Number',
            'constituency_id': 'Constituency',
            'financial_year_id': 'Financial Year',
        }
        widgets = {
            'national_id_no': forms.TextInput(attrs={'class': 'blue-input-box'}),
            'registration_number': forms.TextInput(attrs={'class': 'blue-input-box'}),
            'account_number': forms.TextInput(attrs={'class': 'blue-input-box'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Correctly set the initial value based on the existing instance
        if self.instance and hasattr(self.instance, 'institution_id') and self.instance.institution_id:
            self.fields['institution_id'].initial = self.instance.institution.institution_id
    