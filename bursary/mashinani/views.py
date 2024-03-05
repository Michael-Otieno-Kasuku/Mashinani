import hashlib
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ApplicationForm
from .models import BursaryApplication, Resident, Student, Ward,Account,Bank, FinancialYear
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer
from reportlab.lib.units import inch
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
            national_id_no = form.cleaned_data['national_id_no']
            registration_number = form.cleaned_data['registration_number']
            ward_id = form.cleaned_data['ward_id']
            institution_id = form.cleaned_data['institution_id']
            account_number = form.cleaned_data['account_number']
            financial_year_id = form.cleaned_data['financial_year_id']
            
            # REQ-1: Check for existing application based on the id number, registration number and financial year
            if BursaryApplication.objects.filter(national_id_no=national_id_no,registration_number=registration_number, financial_year_id=financial_year_id).exists():
                form.add_error(None, "You have already applied bursary for this financial year!")

            # REQ-2: Check if the id number provided belongs to that student
            elif not Student.objects.filter(national_id_no=national_id_no, registration_number=registration_number).exists():
                form.add_error(None, "You have provided a wrong registration number or national id number!")

            # REQ-3: Check student registration, i.e., if the applicant is a student of the given institution
            elif not Student.objects.filter(institution_id=institution_id, registration_number=registration_number).exists():
                form.add_error(None, "You have chosen the wrong institution or provided a wrong registration number!")
            
            # REQ-4 Check if the student is indeed a resident of the chosen ward based on the national id number and the chosen ward
            elif not Resident.objects.filter(national_id_no=national_id_no, ward_id=ward_id).exists():
                form.add_error(None, "You have entered a wrong national id number or chosen the wrong ward")
            
            # REQ-5 Check if the provided account number is correct based on the chosen institution
            elif not Account.objects.filter(institution_id=institution_id, account_number=account_number).exists():
                form.add_error(None, "You have entered a wrong account number or chosen the wrong institution")
            
            # REQ-6 Check if the financial year status is open or closed based on the chosen financial year
            elif not FinancialYear.objects.filter(financial_year=financial_year_id, financial_year_status=True).exists():
                form.add_error(None, "The application for the financial year you've chosen is closed!")
            
            else:
                # Generate serial number
                serial_number = generate_serial_number(national_id_no, registration_number, financial_year_id, institution_id)

                # Save the application
                bursary_application = form.save(commit=False)
                bursary_application.serial_number = serial_number
                bursary_application.save()

                return redirect('success_page', serial_number=serial_number)

            # If there are errors, render the template with the form and errors
            return render(request, self.template_name, {'form': form})
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})


class SuccessPageView(View):
    def get(self, request, *args, **kwargs):
        serial_number = self.kwargs.get('serial_number', None)
        return render(request, 'success_page.html', {'serial_number': serial_number})

def generate_serial_number(national_id_no, registration_number, financial_year_id, institution_id):
    data_string = f"{national_id_no}-{registration_number}-{financial_year_id}-{institution_id}"
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
            student = Student.objects.get(registration_number=bursary_application.registration_number)
            account = Account.objects.get(account_number=bursary_application.account_number)
        except BursaryApplication.DoesNotExist:
            return render(request, 'error_page.html')
                
        report_data = {
            'student_details': {
                'first_name':student.first_name,
                'last_name':student.last_name,
                'national_id_no': bursary_application.national_id_no,
                'registration_number': bursary_application.registration_number,
                'institution_id': bursary_application.institution_id,
                'ward_id': bursary_application.ward_id,
            },
            'account_details':{
                'bank_name':account.bank_id,
                'account_number': bursary_application.account_number,
            },
            'application_details':{
                'serial_number': bursary_application.serial_number,
                'financial_year_id': bursary_application.financial_year_id,
                'date_submitted': bursary_application.date_submitted,
            },
            'disbursement_details':{
                'amount_disbursed': bursary_application.amount_disbursed,
                'date_disbursed': bursary_application.date_disbursed,
            },
        }

        # Generate PDF
        pdf_bytes = generate_pdf(report_data)

        # Return the PDF file as a response
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{serial_number}_report.pdf"'
        return response

def generate_pdf(report_data):
    buffer = BytesIO()
    pdf_canvas = SimpleDocTemplate(buffer, pagesize = landscape(letter))

    #Define table data
    table_data = [
        ["BURSARY APPLICATION REPORT"],
        ["SECTION A: Student Details"],
        ["First Name:", report_data['student_details']['first_name']],
        ["Last Name:", report_data['student_details']['last_name']],
        ["National ID Number:", report_data['student_details']['national_id_no']],
        ["Registration Number:", report_data['student_details']['registration_number']],
        ["Institution Name:", report_data['student_details']['institution_id']],
        ["Current Ward of Residence:", report_data['student_details']['ward_id']],
        ["SECTION B: Institution Bank Details"],
        ["Bank Name:", report_data['account_details']['bank_name']],
        ["Institution Bank Account Number:", report_data['account_details']['account_number']],
        ['SECTION C: Application Details'],
        ["Application Serial Number:", report_data['application_details']['serial_number']],
        ["Financial Year:", report_data['application_details']['financial_year_id']],
        ["Date Applied:", report_data['application_details']['date_submitted']],
        ["SECTION D: Disbursement Details"],
        ["Amount Disbursed(Ksh.): ", report_data['disbursement_details']['amount_disbursed']],
        ["Date Disbursed:", report_data['disbursement_details']['date_disbursed']],
    ]
    
    #Create a table
    table = Table(table_data)

    #Set the table style
    # Set table style
    style = TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Header background color
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Content background color
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 12),
                        ('LEFTPADDING', (0, 0), (-1, -1), 10),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                        ('TOPPADDING', (0, 0), (-1, -1), 5),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('SPAN', (0, 0), (1, 0)),  # Merge cells for the heading
                        ])

    table.setStyle(style)

    # Add page border
    frame_styling = TableStyle([('BOX', (0, 0), (-1, -1), 2, colors.black)])
    table.setStyle(frame_styling)

    # Add table to the PDF
    elements = [table]

    # Add space after table
    elements.append(Spacer(1, 0.25 * inch))

    # Build PDF
    pdf_canvas.build(elements)

    # Save the PDF file
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes