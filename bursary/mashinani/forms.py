"""
Module description: Contains classes and forms related to anomaly detection and machine learning models.
"""

from django import forms
from sklearn.ensemble import IsolationForest
from sklearn.base import TransformerMixin
from .models import BursaryApplication, Institution, FinancialYear, Constituency
import joblib

class AnomalyDetector:
    """
    Anomaly detection using Isolation Forest.

    This class provides an anomaly detection mechanism using the Isolation Forest algorithm.
    Anomalies are detected by isolating instances that are significantly different from the majority.
    """

    def __init__(self):
        """
        Initialize the AnomalyDetector with an Isolation Forest model.
        """
        self.model = IsolationForest(contamination=0.05)

    def detect_anomalies(self, data):
        """
        Detect anomalies in the given data.

        Parameters:
        - data (list): List of data points for anomaly detection.

        Returns:
        - list: Anomaly predictions for each data point.
        """
        return self.model.fit_predict(data)

class RegistrationNumberModel(TransformerMixin):
    """
    Feature extraction from registration numbers.

    This transformer class extracts features from student registration numbers.
    The current implementation uses a simple placeholder logic for feature extraction.
    Replace this with a more sophisticated logic for better feature representation.
    """

    def fit(self, X, y=None):
        """
        Fit method for compatibility.

        Parameters:
        - X: Input data.
        - y: Target labels.

        Returns:
        - self: The instance itself.
        """
        return self

    def transform(self, X):
        """
        Transform registration numbers into features.

        Parameters:
        - X: Input data (registration numbers).

        Returns:
        - list: Transformed features for each registration number.
        """
        # Placeholder logic for feature extraction
        # Replace this with your actual feature extraction logic
        return [[len(registration_number)] for registration_number in X]

class MachineLearningModel:
    """
    Machine Learning model for fraud and account validation.

    This class encapsulates a machine learning model for predicting fraudulent registration numbers
    and validating account numbers. Trained models are loaded from file or can be trained within this class.

    The fraud model uses features extracted from registration numbers to predict anomalies, enhancing fraud detection.
    The account model validates institution account numbers, contributing to better data integrity.
    """

    def __init__(self):
        """
        Initialize the MachineLearningModel with trained fraud and account models.
        """
        # Load the trained models from file or train them here
        self.fraud_model = joblib.load('fraud_model.joblib')
        self.account_model = joblib.load('account_model.joblib')

    def predict_fraudulent_registration(self, registration_number):
        """
        Predict if a registration number is fraudulent.

        Parameters:
        - registration_number (str): Student registration number.

        Returns:
        - bool: True if the model predicts anomaly, else False.
        """
        # Feature extraction from the registration number
        features = RegistrationNumberModel().transform([registration_number])

        # Use the trained model to predict fraudulence
        prediction = self.fraud_model.predict(features)

        # For simplicity, return True if the model predicts anomaly (-1)
        return prediction[0] == -1

    def predict_account_number_validity(self, account_number):
        """
        Predict if an account number is valid.

        Parameters:
        - account_number (str): Institution account number.

        Returns:
        - bool: True if the account number is predicted to be valid, else False.
        """
        # Placeholder logic for account number validation
        # Replace this with your actual account number validation logic
        # For simplicity, always return True in this example
        return True

class ApplicationForm(forms.ModelForm):
    """
    Django form for BursaryApplication with anomaly detection and machine learning-based checks.

    This form extends the standard Django ModelForm for BursaryApplication
    and includes additional functionality for anomaly detection and machine learning-based validation.

    Anomalies in the National ID are detected using the AnomalyDetector class.
    Fraudulent registration numbers and invalid account numbers are predicted using the MachineLearningModel class.

    These checks contribute to a more robust and secure data entry process for BursaryApplications.
    """

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
        """
        Initialize the form instance.

        Parameters:
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        
        # Correctly set the initial value based on the existing instance
        if self.instance and hasattr(self.instance, 'institution_id') and self.instance.institution_id:
            self.fields['institution_id'].initial = self.instance.institution.institution_id

    def add_error_with_context(self, field, error_code, message):
        """
        Add a custom error with context to the form.

        Parameters:
        - field (str): Form field name.
        - error_code (str): Error code.
        - message (str): Error message.
        """
        self.add_error(field, forms.ValidationError(message, code=error_code))

    def clean(self):
        """
        Perform data cleaning and machine learning-based checks.

        Returns:
        - dict: Cleaned and validated data.
        """
        cleaned_data = super().clean()
        national_id_no = cleaned_data.get('national_id_no')
        registration_number = cleaned_data.get('registration_number')
        account_number = cleaned_data.get('account_number')

        # Perform machine learning-based anomaly detection here
        anomaly_detector = AnomalyDetector()
        data_for_anomaly_detection = [[national_id_no, registration_number, account_number]]
        anomalies = anomaly_detector.detect_anomalies(data_for_anomaly_detection)

        if anomalies[0] == -1:
            self.add_error_with_context('national_id_no', 'anomaly_detected', "Anomaly detected in the National ID.")

        # Additional machine learning-based checks
        ml_model = MachineLearningModel()

        # Check for fraudulent registration numbers
        if ml_model.predict_fraudulent_registration(registration_number):
            self.add_error_with_context('registration_number', 'fraudulent_registration', "Fraudulent registration number detected.")

        # Check account number validity
        if not ml_model.predict_account_number_validity(account_number):
            self.add_error_with_context('account_number', 'invalid_account_number', "Invalid account number detected.")

        # Additional machine learning-based checks can be added here

        return cleaned_data
