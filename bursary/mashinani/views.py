import hashlib
import uuid
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ApplicationForm
from .models import BursaryApplication, Resident, Student, Ward,Account,Bank, FinancialYear,County, Constituency
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
            ward = Ward.objects.get(ward_name=bursary_application.ward_id)
            constituency = ward.constituency_id
            county = constituency.county_id
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
                'constituency_name': constituency.constituency_name,  # Adding constituency information
                'county_name': county.county_name,  # Adding county information
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

from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.units import inch
from io import BytesIO

def generate_pdf(report_data):
    buffer = BytesIO()
    pdf_canvas = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Define KRA-inspired header and footer styles
    header_style = ParagraphStyle(
        "Header",
        parent=getSampleStyleSheet()["Heading1"],
        fontColor=colors.black,
        fontSize=18,
        spaceAfter=12,
        spaceBefore=12,
        alignment=1,  # Center alignment
    )

    footer_style = ParagraphStyle(
        "Footer",
        parent=getSampleStyleSheet()["Normal"],
        fontColor=colors.black,
        fontSize=14,
        spaceBefore=12,
        alignment=1,  # Center alignment
    )

    # Define header and footer content in KRA style
    header_text = f"<font color='#01689b'>{report_data['student_details']['constituency_name']}</font> NG-CDF Program <font color='#01689b'>{report_data['application_details']['financial_year_id']}</font> Financial Year"
    footer_text = "<font color='#01689b'>© 2024 Bursary Mashinani. All rights reserved.</font>"

    # Create KRA-inspired header and footer paragraphs
    header = Paragraph(header_text, header_style)
    footer = Paragraph(footer_text, footer_style)

    # Create the header and footer space with a touch of elegance
    header_space = Spacer(1, 0.75 * inch)
    footer_space = Spacer(1, 0.75 * inch)

    # Define KRA-inspired table data
    table_data = [
        ["BURSARY APPLICATION REPORT"],
        ["SECTION A: Student Details"],
        ["First Name:", report_data['student_details']['first_name']],
        ["Last Name:", report_data['student_details']['last_name']],
        ["National ID Number:", report_data['student_details']['national_id_no']],
        ["Registration Number:", report_data['student_details']['registration_number']],
        ["Institution Name:", report_data['student_details']['institution_id']],
        ["Current County of Residence:", report_data['student_details']['county_name']],
        ["Current Constituency of Residence:", report_data['student_details']['constituency_name']],
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

    # Create KRA-inspired table
    table = Table(table_data)

    # Set the table style with a KRA touch
    table_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#01689b')),  # Header background color
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Content background color
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, 0), (1, 0)),  # Merge cells for the heading
    ])

    table.setStyle(table_style)

    # Add an exquisite page border
    frame_styling = TableStyle([('BOX', (0, 0), (-1, -1), 2, colors.black)])
    table.setStyle(frame_styling)

    # Add a KRA-inspired watermark
    watermark = Paragraph('<font color="#01689b" size="24">CONFIDENTIAL</font>', getSampleStyleSheet()['Normal'])
    watermark_space = Spacer(1, 1.25 * inch)

    # Add elements to the PDF with a KRA touch
    elements = [header, header_space, table, watermark_space, watermark, footer_space, footer]

    # Build an outstanding PDF
    pdf_canvas.build(elements)

    # Save the exceptional PDF file
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
