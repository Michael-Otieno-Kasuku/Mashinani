from django.test import TestCase
from django.urls import reverse
from .models import BursaryApplication, Voter, Student, Constituency
from .forms import ApplicationForm

class LandingPageViewTest(TestCase):
    def test_landing_page_view(self):
        """Test the LandingPageView."""
        response = self.client.get(reverse('landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')

class ApplicationFormViewTest(TestCase):
    def test_application_form_view_get(self):
        """Test the GET method of ApplicationFormView."""
        response = self.client.get(reverse('application_form'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application_form.html')
        self.assertIsInstance(response.context['form'], ApplicationForm)

    # Add more tests for the POST method of ApplicationFormView if needed

class SuccessPageViewTest(TestCase):
    def test_success_page_view(self):
        """Test the SuccessPageView."""
        serial_number = 'example_serial_number'
        response = self.client.get(reverse('success_page', kwargs={'serial_number': serial_number}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success_page.html')
        self.assertEqual(response.context['serial_number'], serial_number)

class ProgressReportViewTest(TestCase):
    def setUp(self):
        """Set up data for ProgressReportView tests."""
        # Create a sample BursaryApplication instance for testing
        self.bursary_application = BursaryApplication.objects.create(
            # Set necessary fields here
        )

    def test_progress_report_view_get(self):
        """Test the GET method of ProgressReportView."""
        response = self.client.get(reverse('progress_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress_report.html')

    def test_progress_report_view_post(self):
        """Test the POST method of ProgressReportView."""
        # Assuming serial_number is a valid serial number in the database
        data = {'serial_number': self.bursary_application.serial_number}
        response = self.client.post(reverse('progress_report'), data)
        self.assertEqual(response.status_code, 200)
        # Add more assertions based on your expected behavior

# Add more tests for the generate_serial_number and generate_pdf functions if needed
