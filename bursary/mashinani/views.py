import hashlib
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ApplicationForm
from .models import BursaryApplication, Voter, Student, Constituency,Account,Bank
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
            constituency_id = form.cleaned_data['constituency_id']
            institution_id = form.cleaned_data['institution_id']
            account_number = form.cleaned_data['account_number']
            financial_year_id = form.cleaned_data['financial_year_id']
            
            # REQ-1: Check for existing application based on the id number and financial year i.e you can only apply once in every financial year
            if BursaryApplication.objects.filter(national_id_no=national_id_no, financial_year_id=financial_year_id).exists():
                form.add_error(None, "You have already applied bursary for this financial year!")
                return render(request, self.template_name, {'form': form})
            
            # REQ-2: Check if the id number provided is indeed belongs to that particular student
            if not Student.objects.filter(national_id_no=national_id_no,registration_number=registration_number).exists():
                form.add_error(None, "You have provided a wrong registration number or national id number!")
                return render(request, self.template_name, {'form': form})
            
            # REQ-3: Check student registration i.e if the applicant is indeed a student of the given institution based on the reg no and institution id
            if not Student.objects.filter(institution_id=institution_id, registration_number=registration_number).exists():
                form.add_error(None, "You have chosen a wrong institution or you have provided a wrong registration number!")
                return render(request, self.template_name, {'form': form})

            # REQ-4 Check voter eligibility based on the id number and constituency i.e you can only apply if you are a voter in the chosen constituency
            if not Voter.objects.filter(national_id_no=national_id_no, constituency_id=constituency_id).exists():
                form.add_error(None, "You have entered a wrong national id number or you have entered a wrong constituency name!")
                return render(request, self.template_name, {'form': form})
            
            # REQ-5 Check if the provided account number is correct i.e the account number provided should belong to that particular institution that the user entered
            if not Account.objects.filter(institution_id=institution_id, account_number=account_number).exists():
                form.add_error(None, "You have entered a wrong accounter number or you have chosen the wrong institution")
                return render(request, self.template_name, {'form': form})

            # Generate serial number
            serial_number = generate_serial_number(national_id_no, registration_number, financial_year_id, institution_id)

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
                'constituency_id': bursary_application.constituency_id,
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
        ["Constituency Name:", report_data['student_details']['constituency_id']],
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
