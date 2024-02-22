import hashlib
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ApplicationForm
from .models import BursaryApplication, Voter, Student, Constituency
from django.http import HttpResponse
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

class LandingPageView(View):
    def get(self, request):
        return render(request, 'landing_page.html')

class ApplicationFormView(View):
    template_name = 'application_form.html'
    
    def get(self, request):
        form = ApplicationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ApplicationForm(request.POST)

        if form.is_valid():
            voter_id = form.cleaned_data['voter_id']
            student_id = form.cleaned_data['student_id']
            financial_year_id = form.cleaned_data['financial_year_id']
            institution_id = form.cleaned_data['institution_id']

            # Check for existing application
            if BursaryApplication.objects.filter(voter_id=voter_id, student_id=student_id, financial_year_id=financial_year_id).exists():
                form.add_error(None, "This National ID and Student Registration Number have already been used for this financial year.")
                return render(request, self.template_name, {'form': form})

            # Check voter eligibility
            if not Voter.objects.filter(voter_id=voter_id, constituency_id=constituency_id).exists():
                form.add_error(None, "You are not eligible as a voter in Kisumu West Constituency.")
                return render(request, self.template_name, {'form': form})

            # Check student registration
            if not Student.objects.filter(institution_id=institution_id, student_id=student_id).exists():
                form.add_error(None, "Student Registration Number does not exist in the current students register for the chosen institution.")
                return render(request, self.template_name, {'form': form})

            # Generate serial number
            serial_number = generate_serial_number(voter_id, student_id, financial_year_id, institution_id)

            # Save the application
            bursary_application = form.save(commit=False)
            bursary_application.serial_number = serial_number
            bursary_application.save()

            return redirect('success_page', serial_number=serial_number)
        else:
            return render(request, self.template_name, {'form': form})

class SuccessPageView(View):
    def get(self, request, *args, **kwargs):
        serial_number = self.kwargs.get('serial_number', None)
        return render(request, 'success_page.html', {'serial_number': serial_number})

def generate_serial_number(voter_id, student_id, financial_year_id, institution_id):
    data_string = f"{voter_id}-{student_id}-{financial_year_id}-{institution_id}"
    unique_identifier = str(uuid.uuid4())
    combined_string = f"{data_string}-{unique_identifier}"
    serial_number = hashlib.md5(combined_string.encode()).hexdigest()
    return serial_number

class ProgressReportView(View):
    def get(self, request):
        return render(request, 'progress_report.html')

    def post(self, request):
        serial_number = request.POST.get('serial_number')
        try:
            bursary_application = BursaryApplication.objects.get(serial_number=serial_number)
        except BursaryApplication.DoesNotExist:
            return render(request, 'progress_report.html', {'error_message': f'Bursary application with serial number "{serial_number}" not found.'})

        report_data = {
            'student_details': {
                'voter_id': bursary_application.voter_id,
                'student_id': bursary_application.student_id,
            },
            'voter_id': bursary_application.voter_id,
            'institution_id': bursary_application.institution_id,
            'account_id': bursary_application.account_id,
            'financial_year_id': bursary_application.financial_year_id,
            'serial_number': bursary_application.serial_number,
            'date_submitted': bursary_application.date_submitted,
            'amount_disbursed': bursary_application.amount_disbursed,
            'date_disbursed': bursary_application.date_disbursed,
        }

        # Generate PDF
        pdf_bytes = generate_pdf(report_data)

        # Return the PDF file as a response
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{serial_number}_report.pdf"'
        return response

def generate_pdf(report_data):
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)

    # Set font and size
    pdf_canvas.setFont("Helvetica", 12)

    # Add content to the PDF
    pdf_canvas.drawString(100, 770, f"BURSARY APPLICATION REPORT")
    pdf_canvas.drawString(100, 750, f"National ID Number: {report_data['student_details']['voter_id']}")
    pdf_canvas.drawString(100, 730, f"Student Registration Number: {report_data['student_details']['student_id']}")
    pdf_canvas.drawString(100, 710, f"Constituency: {report_data['constituency_id']}")
    pdf_canvas.drawString(100, 690, f"Institution Name: {report_data['institution_id']}")
    pdf_canvas.drawString(100, 670, f"Account Number: {report_data['account_id']}")
    pdf_canvas.drawString(100, 650, f"Financial Year: {report_data['financial_year_id']}")
    pdf_canvas.drawString(100, 630, f"Serial Number: {report_data['serial_number']}")
    pdf_canvas.drawString(100, 610, f"Date Applied: {report_data['date_submitted']}")
    pdf_canvas.drawString(100, 590, f"Amount Disbursed: {report_data['amount_disbursed']}")
    pdf_canvas.drawString(100, 570, f"Date Disbursed: {report_data['date_disbursed']}")

    # Save the PDF file
    pdf_canvas.save()

    # Get the value of the BytesIO buffer and reset the buffer position
    pdf_bytes = buffer.getvalue()
    buffer.seek(0)

    return pdf_bytes
