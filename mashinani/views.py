from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import ApplicationForm, RegisterForm, LoginForm, PasswordResetForm
from .models import Bank, Institution, Account,Country, Region, County, Constituency, Ward, Student, FinancialYear,Resident, BursaryApplication, User,PasswordResetToken
from django.http import HttpResponse
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
import hashlib
import uuid
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data['email_address']
            password = form.cleaned_data['password']
            user = User.objects.filter(email_address=email_address).first()
            if user and user.check_password(password):
                # Authentication successful
                request.session['email_address'] = user.email_address
                return redirect('landing_page')
            else:
                # Authentication failed
                form.add_error(None, "Incorrect email address or password!")
                return render(request, self.template_name, {'form': form}, status=400)
        else:
            return render(request, self.template_name, {'form': form}, status=400)

class RegisterView(View):
    template_name = 'signup.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            national_id_no = form.cleaned_data['national_id_no']
            email_address = form.cleaned_data['email_address']
            password_hash = form.cleaned_data['password_hash']

            # Check if account already exists
            if User.objects.filter(email_address=email_address).exists():
                form.add_error(None, "This email address has already been used!")
                return render(request, self.template_name, {'form': form})
            else:
                # Create the account
                new_account = form.save(commit=False)
                new_account.set_password(password_hash)
                new_account.save()

                # Redirect to success page
                return redirect('register_success')
        else:
            # If the form is not valid, render the template with the form and errors
            return render(request, self.template_name, {'form': form})

class RegisterSuccessPageView(View):
    def get(self, request):
        return render(request, 'register_success.html')

class PasswordResetView(View):
    template_name = 'forgot_password.html'

    def get(self, request):
        form = PasswordResetForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            email_address = form.cleaned_data['email_address']

            # REQ-1: Check if the email address exists
            if not User.objects.filter(email_address=email_address).exists():
                form.add_error(None, "Invalid email address!")
            else:
                # Generate a unique token
                token = get_random_string(length=32)

                # Store the token along with the user's email address and expiration timestamp
                PasswordResetToken.objects.create(
                    email=email_address,
                    token=token,
                    expiry_timestamp=timezone.now() + timezone.timedelta(hours=1)  # Token expires in 1 hour
                )

                # Construct the password reset link
                reset_link = request.build_absolute_uri(f'/password-reset/{token}')

                # Send email with the reset link
                send_mail(
                    'Password Reset Link',
                    f'Click the following link to reset your password: {reset_link}',
                    'michaelotienokasuku@gmail.com',
                    [email_address],
                    fail_silently=False,
                )

                # Redirect to a success page or display a success message
                return redirect('password_reset_success',email_address=email_address)
            
        # If there are errors, render the template with the form and errors
        return render(request, self.template_name, {'form': form})

class PasswordResetSuccessView(View):
    def get(self, request, *args, **kwargs):
        email_address = self.kwargs.get('email_address', None)
        return render(request, 'password_reset_success.html', {'email_address': email_address})

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
            # Form is valid, proceed with processing data
            national_id_no = form.cleaned_data['national_id_no']
            registration_number = form.cleaned_data['registration_number']
            ward_id = form.cleaned_data['ward_id']
            institution_id = form.cleaned_data['institution_id']
            account_number = form.cleaned_data['account_number']
            financial_year_id = form.cleaned_data['financial_year_id']
            
            # Check for existing application based on the id number, registration number and financial year
            if BursaryApplication.objects.filter(national_id_no=national_id_no, registration_number=registration_number, financial_year_id=financial_year_id).exists():
                form.add_error(None, "You have already applied for bursary for this financial year!")

            # Check if the id number provided belongs to that student
            elif not Student.objects.filter(national_id_no=national_id_no, registration_number=registration_number).exists():
                form.add_error(None, "You have provided a wrong registration number or national id number!")

            # Check student registration, i.e., if the applicant is a student of the given institution
            elif not Student.objects.filter(institution_id=institution_id, registration_number=registration_number).exists():
                form.add_error(None, "You have chosen the wrong institution or provided a wrong registration number!")
            
            # Check if the student is indeed a resident of the chosen ward based on the national id number and the chosen ward
            elif not Resident.objects.filter(national_id_no=national_id_no, ward_id=ward_id).exists():
                form.add_error(None, "You have entered a wrong national id number or chosen the wrong ward")
            
            # Check if the provided account number is correct based on the chosen institution
            elif not Account.objects.filter(institution_id=institution_id, account_number=account_number).exists():
                form.add_error(None, "You have entered a wrong account number or chosen the wrong institution")
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

class SuccessPageView(View):
    def get(self, request, *args, **kwargs):
        serial_number = self.kwargs.get('serial_number', None)
        return render(request, 'success_page.html', {'serial_number': serial_number})

def generate_serial_number(national_id_no, registration_number, financial_year_id, institution_id):
    data_string = f"{national_id_no}-{registration_number}-{financial_year_id}-{institution_id}"
    unique_identifier = str(uuid.uuid4())
    combined_string = f"{data_string}-{unique_identifier}"
    hashed_serial = hashlib.sha256(combined_string.encode()).hexdigest()
    truncated_hash = hashed_serial[:10]
    return truncated_hash

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
                'constituency_name': constituency.constituency_name,
                'county_name': county.county_name,
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
    pdf_canvas = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.textColor = colors.black  # Black font color
    title_style.alignment = 1  # Center alignment
    title_style.fontSize = 28

    subtitle_style = styles['Heading2']
    subtitle_style.textColor = colors.black  # Black font color
    subtitle_style.alignment = 1  # Center alignment
    subtitle_style.fontSize = 24

    section_header_style = styles['Heading3']
    section_header_style.textColor = colors.black  # Black font color
    section_header_style.fontSize = 20

    # Define paragraph styles
    paragraph_style = ParagraphStyle(
        "Normal",
        fontSize=18,
        leading=18,
        textColor="black",
        alignment=0  # 0 for left alignment, 1 for center, 2 for right
    )

    footer_style = styles['Normal']
    footer_style.alignment = 1  # Center alignment

    # Define footer content
    footer_text = "<font color='#01689b'>© 2024 Bursary Mashinani. All rights reserved.</font>"

    # Create footer paragraph
    footer = Paragraph(footer_text, footer_style)

    # Create title
    title_text = f"<font color='#01689b'>{report_data['student_details']['constituency_name']}</font> NG-CDF <font color='#01689b'>{report_data['application_details']['financial_year_id']}</font> Financial Year"
    title = Paragraph(title_text, title_style)

    # Create subtitle
    subtitle_text = "Bursary Application Report"
    subtitle = Paragraph(subtitle_text, subtitle_style)

    # Define sections
    sections = [
        ("<p>SECTION A: Student Details", [
            f"<p><b>First Name:</b> {report_data['student_details']['first_name']}</p>",
            f"<p><b>Last Name:</b> {report_data['student_details']['last_name']}</p>",
            f"<p><b>National ID Number:</b> {report_data['student_details']['national_id_no']}</p>",
            f"<p><b>Registration Number:</b> {report_data['student_details']['registration_number']}</p>",
            f"<p><b>Institution Name:</b> {report_data['student_details']['institution_id']}</p>",
            f"<p><b>Current County of Residence:</b> {report_data['student_details']['county_name']}</p>",
            f"<p><b>Current Constituency of Residence:</b> {report_data['student_details']['constituency_name']}</p>",
            f"<p><b>Current Ward of Residence:</b> {report_data['student_details']['ward_id']}</p>"
        ]),
        ("<p>SECTION B: Institution Bank Details", [
            f"<p><b>Bank Name:</b> {report_data['account_details']['bank_name']}</p>",
            f"<p><b>Institution Bank Account Number:</b> {report_data['account_details']['account_number']}</p>"
        ]),
        ("<p>SECTION C: Bursary Application Details", [
            f"<p><b>Application Serial Number:</b> {report_data['application_details']['serial_number']}</p>",
            f"<p><b>Financial Year:</b> {report_data['application_details']['financial_year_id']}</p>",
            f"<p><b>Date Applied:</b> {report_data['application_details']['date_submitted']}</p>"
        ]),
        ("<p>SECTION D: Bursary Disbursement Details", [
            f"<p><b>Amount Disbursed(Ksh.):</b> {report_data['disbursement_details']['amount_disbursed']}</p>",
            f"<p><b>Date Disbursed:</b> {report_data['disbursement_details']['date_disbursed']}</p>"
        ])
    ]

    # Create elements
    elements = [title, Spacer(1, 0.25 * inch), subtitle, Spacer(1, 0.5 * inch)]

    # Add sections to the PDF
    for section_title, section_content in sections:
        elements.append(Paragraph(section_title, section_header_style))
        elements.extend([Paragraph(content, paragraph_style) for content in section_content])
        elements.append(Spacer(1, 0.25 * inch))

    elements.append(footer)

    # Build PDF
    pdf_canvas.build(elements)

    # Save PDF file
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
