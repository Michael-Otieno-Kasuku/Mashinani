from django import forms
from .models import BursaryApplication, Institution, FinancialYear, Constituency

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
        fields = ['voter_id', 'student_id', 'institution_id', 'account_id','constituency_id', 'financial_year_id']
        labels = {
            'voter_id': 'National ID Number',
            'student_id': 'Student Registration Number',
            'institution_id': 'Institution Name',
            'account_id': 'Institution Account Number',
            'constituency_id': 'Constituency',
            'financial_year_id': 'Financial Year',
        }
        widgets = {
            'voter_id': forms.TextInput(attrs={'class': 'blue-input-box'}),
            'student_id': forms.TextInput(attrs={'class': 'blue-input-box'}),
            'account_id': forms.TextInput(attrs={'class': 'blue-input-box'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Correctly set the initial value based on the existing instance
        if self.instance and hasattr(self.instance, 'institution_id') and self.instance.institution_id:
            self.fields['institution_id'].initial = self.instance.institution.institution_id
        

class ProgressTrackingForm(forms.Form):
    serial_number = forms.CharField(
        max_length=8,
        help_text="Enter the 8-alphanumeric serial number",
        widget=forms.TextInput(attrs={'class': 'blue-input-box'})
    )
