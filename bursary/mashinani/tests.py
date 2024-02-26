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
        response = self.client.get(reverse('apply'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application_form.html')
        self.assertIsInstance(response.context['form'], ApplicationForm)

class SuccessPageViewTest(TestCase):
    def test_success_page_view(self):
        """Test the SuccessPageView."""
        serial_number = '8ee7b150b91f7394afbd67221db438f7'
        response = self.client.get(reverse('success_page', kwargs={'serial_number': serial_number}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success_page.html')
        self.assertEqual(response.context['serial_number'], serial_number)
