from django.db import models,transaction
from decimal import Decimal
import re
from datetime import timedelta
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
import random
import string
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.db.models import Max
from datetime import date
import datetime





## insurance
class AllInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15, unique=True)
    email_id = models.EmailField()
    messgae=models.TextField()

    def __str__(self) :
        return f"{self.insurance_name} -{self.name}"
    
class LifeInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15, unique=True)
    email_id = models.EmailField()
    messgae=models.TextField()

    def __str__(self) :
        return f"{self.insurance_name} -{self.name}" 

class GeneralInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15, unique=True)
    email_id = models.EmailField()
    messgae=models.TextField()

    def __str__(self) :
        return f"{self.insurance_name} -{self.name}" 

class healthInsurance(models.Model):
    insurance_name=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    mobile_number=models.CharField(max_length=15, unique=True)
    email_id = models.EmailField()
    messgae=models.TextField()

    def __str__(self) :
        return f"{self.insurance_name} -{self.name}" 


# Custom validators

def validate_only_letters(value):
    if not value.isalpha() and r'^\s{100}$':
        raise ValidationError('Only letters are allowed.')
    
def validate_pan(value):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid PAN number format')

def validate_mobile_number(value):
    
    if len(value)!=10 or not value.isdigit():
        raise ValidationError('Invalid mobile number format')

# def validate_aadhar_number(value):
#       # Convert the value to a string
#     if len(value) != 12 or not value.isdigit():
#         raise ValidationError('Invalid Aadhar number format. It should be exactly 12 digits and contain only numbers.')

def validate_pincode(value):
    pattern = r'^\d{6}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid pincode format')



def validate_amount(value):
    if len(str(value)) > 10:
        raise ValidationError('Amount must be 10 digits.')
    
def validate_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date should be in the past or present.')
def validate_address(value):
    # Check if value contains both letters and digits
    has_letter = re.search(r'[A-Za-z]', value)
    has_digit = re.search(r'\d', value)

    if not (has_letter and has_digit):
        raise ValidationError('Address must contain both letters and digits.')

    
def validate_gst_number(value):
    gst_regex = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$')
    
    value_str = str(value)  # Convert the value to a string
    if not gst_regex.match(value_str):
        raise ValidationError('Invalid GST number format.')

def validate_age(date_of_birth):
    if not isinstance(date_of_birth, date):
        raise ValidationError('Invalid date format.')
    
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if not (18 <= age <= 70):
        raise ValidationError('Age must be between 18 and 70 years.')
    
def validate_email(value):
    # Check for the presence of the '@' symbol
    if "@" not in value:
        raise ValidationError('Invalid email address.')

    # Split the email into local part and domain part
    local_part, domain = value.rsplit('@', 1)

    # Check if domain has a valid extension
    valid_extensions = ['.com', '.in']
    if not any(domain.endswith(ext) for ext in valid_extensions):
        raise ValidationError('Please enter a valid email address with .com or .in domain.')

    # Ensure that the local part contains at least one letter
    if not re.search(r'[a-zA-Z]', local_part):
        raise ValidationError('Email must contain at least one letter before @domain.')

    # Optionally: Ensure the email does not contain invalid characters
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        raise ValidationError('Invalid email address format.')

# Models
class basicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    full_name = models.CharField(max_length=25,validators=[validate_only_letters])
    pan_number = models.CharField(max_length=10, validators=[validate_pan])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    email = models.EmailField(validators=[validate_email])
    date_of_birth = models.DateField(validators=[validate_date])
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='Single')
    required_loan_amount = models.CharField(max_length=10,validators=[validate_amount])
    terms_accepted = models.BooleanField(default=False,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    random_number = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        if not self.random_number:
            self.random_number = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)


class goldbasicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]

    full_name = models.CharField(max_length=25,validators=[validate_only_letters])
    pan_number = models.CharField(max_length=10, validators=[validate_pan])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    email = models.EmailField(validators=[validate_email])
    date_of_birth = models.DateField(validators=[validate_date])
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='Single')
    required_loan_amount = models.IntegerField(validators=[validate_amount])
    terms_accepted = models.BooleanField(default=False,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    random_number = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        if not self.random_number:
            self.random_number = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

class LoanApplication(models.Model):
    LOAN_TYPE_CHOICES = [
        ('LAP', 'Loan Against Property'),
        ('LAPBT', 'Loan Against Property with Business Tenure'),
    ]
    INCOME_SOURCE_CHOICES = [
        ('JOB', 'Job'),
        ('BUSINESS', 'Business'),
    ]

    # Basic Information
    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES)
    first_name = models.CharField(max_length=50,validators=[validate_only_letters])
    last_name = models.CharField(max_length=50,validators=[validate_only_letters])
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    date_of_birth = models.DateField(validators=[validate_date])
    mobile_number = models.CharField(max_length=10, validators=[validate_mobile_number])
    pan_card_number = models.CharField(max_length=10, validators=[validate_pan])
    aadhar_card_number = models.CharField(max_length=12,)
    marital_status = models.CharField(max_length=10, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')])
    email_id = models.EmailField(validators=[validate_email])
    current_address = models.TextField(validators=[validate_address])
    current_address_pincode = models.CharField(max_length=6, validators=[validate_pincode])
    aadhar_address = models.TextField(validators=[validate_address])
    aadhar_pincode = models.CharField(max_length=6, validators=[validate_pincode])

    # Job-related Fields
    income_source = models.CharField(max_length=10, choices=INCOME_SOURCE_CHOICES)
    net_salary_per_month = models.IntegerField(validators=[validate_amount],null=True,blank=True)
    company_name = models.CharField(max_length=100,validators=[validate_only_letters],default='',null=True,blank=True)
    company_type = models.CharField(max_length=50, null=True, blank=True,validators=[validate_only_letters])
    job_joining_date = models.DateField(null=True, blank=True,validators=[validate_date])
    job_location = models.CharField(max_length=100, null=True, blank=True)
    total_job_experience = models.IntegerField(null=True, blank=True)

    # Business-related Fields
    net_income_per_month = models.IntegerField(null=True, blank=True,validators=[validate_amount])
    business_name = models.CharField(max_length=100, null=True, blank=True,validators=[validate_only_letters])
    business_type = models.CharField(max_length=50, null=True, blank=True,validators=[validate_only_letters])
    business_establishment_date = models.DateField(null=True, blank=True,validators=[validate_date])
    gst_certificate = models.BooleanField(default=False, verbose_name="GST Certificate?")
    gst_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="GST Number",validators=[validate_gst_number])
    nature_of_business = models.TextField(null=True, blank=True,validators=[validate_only_letters])
    turnover_in_lakhs_per_year = models.IntegerField(null=True, blank=True,validators=[validate_amount])

    # Additional Fields
    property_value = models.IntegerField(validators=[validate_amount])
    required_loan_amount = models.IntegerField(validators=[validate_amount])
    existing_loan = models.BooleanField(default=False)
    existing_loan_details = models.CharField(max_length=100, null=True, blank=True)
    ref1_name = models.CharField(max_length=100,null=True,blank=True)
    ref1_mobile = models.CharField(max_length=10,null=True,blank=True, validators=[validate_mobile_number])
    ref2_name = models.CharField(max_length=100,null=True,blank=True,validators=[validate_only_letters])
    ref2_mobile = models.CharField(max_length=10,null=True,blank=True, validators=[validate_mobile_number])
    remarks = models.TextField(null=True, blank=True)

    # Co-Applicant Fields
    co_applicant_first_name = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_last_name = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    co_applicant_age = models.DateField(null=False, blank=False, validators=[validate_age], default=datetime.date(2020, 1, 1))
    co_applicant_relationship = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_mobile_number = models.CharField(max_length=10, null=False, blank=False, validators=[validate_mobile_number],default="")
    co_applicant_email_id = models.EmailField(null=False, blank=False, validators=[validate_email],default="@gmail.com")
    co_applicant_occupation = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters],default="")
    co_applicant_net_income_per_month = models.IntegerField(null=False, blank=False,validators=[validate_amount])
    random_number = models.CharField(max_length=10, blank=True, null=True)

    
    def save(self, *args, **kwargs):
        if not self.random_number:
          
            last_entry = LoanApplication.objects.filter(random_number__startswith='SLNPER').order_by('-random_number').first()
            
            if last_entry:
               
                last_number = int(last_entry.random_number[6:])  
                new_number = last_number + 1
            else:
               
                new_number = 1001
            
            
            self.random_number = f"SLNPER{new_number:04d}"
        
        print(f"Saving PersonalDetail with random_number: {self.random_number}")
        super(LoanApplication, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

def validate_image_file(value):
    valid_extensions = ['.jpg', '.jpeg', '.png']
    extension = value.name.split('.')[-1].lower()
    if f".{extension}" not in valid_extensions:
        raise ValidationError('Only JPG, JPEG, and PNG files are allowed.')



def validate_pdf_file(value):
    if not value.name.lower().endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')


class lapDocumentUpload(models.Model):
    personal_details = models.ForeignKey(LoanApplication, on_delete=models.CASCADE)
    adhar_card_front = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    adhar_card_back = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    pan_card = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    customer_photo = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    property_photo1 = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    property_photo2 = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    property_photo3 = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    property_photo4 = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    pay_slips = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    bank_statement = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    employee_id_card = models.ImageField(upload_to='documents/', null=True, blank=True,validators=[validate_image_file])
    business_proof1 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    business_proof2 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    bank_statement_12m = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    business_office_photo = models.ImageField(upload_to='documents/', null=True, blank=True,validators=[validate_image_file])
    itr1 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    itr2 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    itr3 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    address_proof = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    existing_loan_statement = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    other_document1 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    other_document2 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    other_document3 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])
    other_document4 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_pdf_file])

    # Co-applicant documents
    co_applicant_adhar_card_front = models.ImageField(upload_to='documents/adhar_front/',null=False, blank=False,validators=[validate_image_file],default="image")
    co_applicant_adhar_card_back = models.ImageField(upload_to='documents/adhar_back/',null=False, blank=False,validators=[validate_image_file],default="image")
    co_applicant_pan_card = models.ImageField(upload_to='documents/pan_card/',null=False, blank=False,validators=[validate_image_file],default="image")
    co_applicant_selfie_photo = models.ImageField(upload_to='documents/selfie_photo/',null=False, blank=False,validators=[validate_image_file],default="image")


class Goldloanapplication(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False,validators=[validate_only_letters],)
    email = models.EmailField(null=True, blank=True, validators=[validate_email])
    contact_no = models.CharField(
        max_length=10,  # Adjust length as needed
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Contact number must be 10 digits.',
                code='invalid_contact_number'
            )
        ],
        null=False,
        blank=False
    )    
    state = models.CharField(max_length=50, null=False, blank=False,validators=[validate_only_letters])
    pincode = models.CharField(max_length=6, validators=[validate_pincode])

    random_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.random_number:
            # Query to get the last number with the prefix 'SLNLAP-'
            last_entry = Goldloanapplication.objects.filter(random_number__startswith='SLNGLD-').aggregate(Max('random_number'))
            last_number = last_entry['random_number__max']

            if last_number:
                # Extract the number part, increment it, and format the new number
                last_number_int = int(last_number.split('-')[1])  # Split on hyphen and extract number
                new_number = last_number_int + 1
            else:
                # Starting number if no entries exist
                new_number = 1001

            # Set the new random_number with hyphen and zero-padding
            self.random_number = f"SLNGLD-{new_number:04d}"
        
        print(f"Saving LoanApplication with random_number: {self.random_number}")
        super(Goldloanapplication, self).save(*args, **kwargs)


class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=2)
        super().save(*args, **kwargs)


class lapApplicationVerification(models.Model):

    loan= models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='applicationverification',blank=True)
    personal_detail_verifaction=models.CharField(max_length=50,blank=True)
    documents_upload_verification=models.CharField(max_length=50,blank=True)
    kyc_and_document_verification=models.CharField(max_length=50,blank=True)
    field_officer_visit_inspection=models.CharField(max_length=50,blank=True)
    eligibility_check_verification=models.CharField(max_length=50,blank=True)

    Application_fee_paid=models.CharField(max_length=50,blank=True)
    tele_verification=models.CharField(max_length=50,blank=True)
    bank_login_fee_paid=models.CharField(max_length=50,blank=True)
    bank_login_done=models.CharField(max_length=50,blank=True)
    credit_manager_visit=models.CharField(max_length=50,blank=True)
    bank_or_nbfc_soft_loan_sanctioned=models.CharField(max_length=50,blank=True)
    final_loan_sanctioned=models.CharField(max_length=50,blank=True)
    legal_techinal_completed=models.CharField(max_length=50,blank=True)
    agreement_signatures_done=models.CharField(max_length=50,blank=True)
    enach_verification=models.CharField(max_length=50,blank=True)
    disbursment_verification=models.CharField(max_length=50,blank=True)
    post_documentation=models.CharField(max_length=100,blank=True)
    cheque_issued=models.CharField(max_length=100,blank=True)
    total_application_status=models.CharField(max_length=100,blank=True)


# =====================bhanu===========================================











    




    

   
    