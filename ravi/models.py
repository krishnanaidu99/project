from django.db import models
from django.core.validators import EmailValidator
import random
import string
import re
from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_only_letters(value):
    if not value.isalpha():
        raise ValidationError('Only letters are allowed.')
    
def validate_pan(value):
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid PAN number format')

def validate_mobile_number(value):
    pattern = r'^\+?[1-9]\d{1,14}$'
    if not re.match(pattern, value) or len(value) < 10:
        raise ValidationError('Invalid mobile number format. Must be at least 10 digits long.')
    if len(value) > 15:
        raise ValidationError('Mobile number cannot be more than 15 digits long.')

def validate_aadhar_number(value):
    pattern = r'^\d{12}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid Aadhar number format')

def validate_pincode(value):
    pattern = r'^\d{6}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid pincode format')

def validate_pincodes(value):
    if len(str(value)) != 6:
        raise ValidationError('Pincode must be 6 digits.')

def validate_amount(value):
    if len(str(value)) > 10:
        raise ValidationError('Amount must be 10 digits.')
    
def clean_aadhar_card_front(self):
        file = self.cleaned_data.get('aadhar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg'):
                raise ValidationError(('Only JPG/JPEG/ files are allowed.'), code='invalid')
        return file
def clean_business_proof_1(self):
        file = self.cleaned_data.get('business_proof_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(('Only PDF files are allowed.'), code='invalid')
        return file
def validate_image_file(value):
    if not (value.name.endswith('.jpg') or value.name.endswith('.png') or value.name.endswith('.jpeg')):
        raise ValidationError('Only JPG/JPEG/PNG files are allowed.')


def validate_pdf_file(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')
def validate_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')
def validate_gst_number(value):
    gst_regex = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$')
    if not gst_regex.match(value):
        raise ValidationError('Invalid GST number format.')


from datetime import date
def validate_age(value):
    try:
        age = int(value)
    except (ValueError, TypeError):
        raise ValidationError('Age must be a number.')
    if not (18 <= age <= 70):
        raise ValidationError('Age must be between 18 and 70.')
def validate_address(value):
    
    has_letter = re.search(r'[A-Za-z]', value)
    has_digit = re.search(r'\d', value)

    if not (has_letter and has_digit):
        raise ValidationError('Address must contain both letters and digits.')

    
def validate_email(value):
    if "@" not in value:
        raise ValidationError('Invalid email address.')

    local_part, domain = value.split('@')
    
    if domain != "gmail.com":
        raise ValidationError('Email domain must be gmail.com.')
    
    if not re.search(r'[a-zA-Z]', local_part):
        raise ValidationError('Email must contain at least one letter before @gmail.com.')


class plbasicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    full_name = models.CharField(max_length=25, validators=[validate_only_letters])
    pan_number = models.CharField(max_length=10, validators=[validate_pan])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    email = models.EmailField(validators=[validate_email])
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='Single')
    required_loan_amount = models.CharField(max_length=10, validators=[validate_amount])
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    random_number = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        if not self.random_number:
            self.random_number = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)


class hlbasicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    full_name = models.CharField(max_length=25, validators=[validate_only_letters])
    pan_number = models.CharField(max_length=10, validators=[validate_pan])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    email = models.EmailField(validators=[validate_email])
    date_of_birth = models.DateField()
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='Single')
    required_loan_amount = models.CharField(max_length=10, validators=[validate_amount])
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    random_number = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    def save(self, *args, **kwargs):
        if not self.random_number:
            self.random_number = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

class PersonalDetail(models.Model):
    GENDER_CHOICES = [
        ('FEMALE', 'Female'),
        ('MALE', 'Male'),
        ('OTHER', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('SINGLE', 'Single'),
        ('MARRIED', 'Married'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('GOVERNMENT', 'Government'),
        ('SELF_EMPLOYED', 'Self-employed'),
        ('OTHER', 'Other'),
    ]

    first_name = models.CharField(max_length=100, validators=[validate_only_letters])
    last_name = models.CharField(max_length=100, validators=[validate_only_letters])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    father_name = models.CharField(max_length=100,validators=[validate_only_letters])
    date_of_birth = models.DateField(validators=[validate_date])
    mobile_number = models.CharField(max_length=10, validators=[validate_mobile_number])
    pan_card_number = models.CharField(max_length=10, validators=[validate_pan])
    aadhar_card_number = models.CharField(max_length=12, validators=[validate_aadhar_number])
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    email = models.EmailField(validators=[validate_email])
    current_address = models.TextField(validators=[validate_address])
    current_address_pincode = models.CharField(max_length=6,validators= [validate_pincode])
    aadhar_address = models.TextField(validators=[validate_address])
    aadhar_pincode = models.CharField(max_length=6,validators= [validate_pincode])
    running_emis = models.CharField(max_length=10, validators=[validate_amount])
    net_salary = models.CharField(max_length=10, validators=[validate_amount])
    company_name = models.CharField(max_length=100,validators=[validate_only_letters])
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES)
    job_joining_date = models.DateField()
    job_location = models.CharField(max_length=100)
    total_job_experience = models.IntegerField()
    work_email = models.EmailField(validators=[validate_email])
    office_address = models.TextField(validators=[validate_address])
    office_address_pincode = models.CharField(max_length=6,validators= [validate_pincode])
    required_loan_amount = models.CharField(max_length=10, validators=[validate_amount])
    ref1_name = models.CharField(max_length=100,validators=[validate_only_letters])
    ref1_mobile = models.CharField(max_length=10, validators=[validate_mobile_number])
    ref2_name = models.CharField(max_length=100,validators=[validate_only_letters])
    ref2_mobile = models.CharField(max_length=10, validators=[validate_mobile_number])
    own_house = models.BooleanField()
    random_number = models.CharField(max_length=10, blank=True, null=True)





    def save(self, *args, **kwargs):
        if not self.random_number:
          
            last_entry = PersonalDetail.objects.filter(random_number__startswith='SLNPER').order_by('-random_number').first()
            
            if last_entry:
               
                last_number = int(last_entry.random_number[6:])  
                new_number = last_number + 1
            else:
               
                new_number = 1001
            
            
            self.random_number = f"SLNPER{new_number:04d}"
        
        print(f"Saving PersonalDetail with random_number: {self.random_number}")
        super(PersonalDetail, self).save(*args, **kwargs)





class DocumentUpload(models.Model):
    personal_detail = models.ForeignKey(PersonalDetail, on_delete=models.CASCADE)
    aadhar_card_front = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    aadhar_card_back = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    pan_card = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    customer_photo = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    payslip_1 = models.FileField(upload_to='documents/',validators=[validate_pdf_file])
    payslip_2 = models.FileField(upload_to='documents/',validators=[validate_pdf_file])
    payslip_3 = models.FileField(upload_to='documents/',validators=[validate_pdf_file])
    bank_statement = models.FileField(upload_to='documents/',validators=[validate_pdf_file])
    employee_id_card = models.ImageField(upload_to='documents/',validators=[validate_image_file])
    current_address_proof = models.FileField(upload_to='documents/',validators=[validate_image_file])
    other_document_1 = models.FileField(upload_to='documents/', blank=True, null=True,validators=[validate_pdf_file])
    other_document_2 = models.FileField(upload_to='documents/', blank=True, null=True,validators=[validate_pdf_file])

    def __str__(self):
        return f"{self.personal_detail.first_name} {self.personal_detail.last_name} - Documents"


class ApplicationVerification(models.Model):
   

    personal_detail = models.ForeignKey(PersonalDetail, on_delete=models.CASCADE) 
    personal_detail_verification = models.CharField(max_length=50, blank=True, )
    documents_upload_verification = models.CharField(max_length=50, blank=True, )
    documents_verification = models.CharField(max_length=50, blank=True, )
    eligibility_check_verification = models.CharField(max_length=50, blank=True, )
    bank_login_verification = models.CharField(max_length=50, blank=True, )
    kyc_and_document_verification = models.CharField(max_length=50, blank=True, )
    enach_verification = models.CharField(max_length=50, blank=True, )
    disbursement_verification = models.CharField(max_length=50, blank=True, )
    verification_status = models.CharField(max_length=100, blank=True,)

    def __str__(self):
        return f"ApplicationVerification for {self.personal_detail} - Status: {self.verification_status}"

#homeloan=============
class CustomerProfile(models.Model):
    LOAN_TYPE_CHOICES = [('HL', 'HL'), ('HLBT', 'HLBT')]
    INCOME_SOURCE_CHOICES = [('Job', 'Job'), ('Business', 'Business')]
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    COMPANY_TYPE_CHOICES = [
        ('Private', 'Private'),
        ('Public', 'Public'),
        ('Government', 'Government'),
        ('Other', 'Other'),
    ]
    BUSINESS_TYPE_CHOICES = [
        ('Retail', 'Retail'),
        ('Manufacturing', 'Manufacturing'),
        ('Services', 'Services'),
        ('Other', 'Other'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    loan_type = models.CharField(max_length=10, choices=LOAN_TYPE_CHOICES)
    first_name = models.CharField(max_length=100, validators=[validate_only_letters])
    last_name = models.CharField(max_length=100, validators=[validate_only_letters])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(validators=[validate_date])
    mobile_number = models.CharField(max_length=10, validators=[validate_mobile_number])
    pan_card_number = models.CharField(max_length=10, validators=[validate_pan])
    aadhar_card_number = models.CharField(max_length=12, validators=[validate_aadhar_number])
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    email_id = models.EmailField(validators=[validate_email])
    current_address = models.TextField()
    current_address_pincode = models.CharField(max_length=6, validators=[validate_pincode])
    aadhar_address = models.TextField()
    aadhar_pincode = models.CharField(max_length=6, validators=[validate_pincode])
    running_emis_per_month = models.CharField(max_length=10, validators=[validate_amount])
    income_source = models.CharField(max_length=10, choices=INCOME_SOURCE_CHOICES)
    # Job-related fields
    net_salary_per_month = models.CharField(max_length=10, blank=True, null=True, validators=[validate_amount])
    company_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_only_letters])
    company_type = models.CharField(max_length=50, choices=COMPANY_TYPE_CHOICES, blank=True, null=True)
    job_joining_date = models.DateField(blank=True, null=True,)
    job_location = models.CharField(max_length=100, blank=True, null=True)
    total_job_experience = models.IntegerField(blank=True, null=True)
    work_email = models.EmailField(blank=True, null=True)
    office_address_pincode = models.CharField(max_length=6, blank=True, null=True, validators=[validate_pincode])
    # Business-related fields
    net_income_per_month = models.CharField(max_length=10, blank=True, null=True, validators=[validate_amount])
    business_name = models.CharField(max_length=100, blank=True, null=True, validators=[validate_only_letters])
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True)
    business_establishment_date = models.DateField(blank=True, null=True)
   
    gst_number = models.CharField(max_length=15, blank=True, null=True , validators=[validate_gst_number])
    mother_name = models.CharField(max_length=100,validators=[validate_only_letters])
    father_name = models.CharField(max_length=100, validators=[validate_only_letters])
    nature_of_business = models.CharField(max_length=100, blank=True, null=True)
    turnover_per_year = models.CharField(max_length=10, blank=True, null=True, validators=[validate_amount])
    business_address_pincode = models.CharField(max_length=6, blank=True, null=True, validators=[validate_pincode])
    house_plot_purchase_value = models.CharField(max_length=10,default='', blank=False, null=False, validators=[validate_amount])
    required_loan_amount = models.CharField(max_length=10,default='', blank=False, null=False, validators=[validate_amount])
   
    existing_loan_bank_nbfc_name = models.CharField(max_length=100, blank=False, null=False,default='')
    existing_loan_amount = models.CharField(max_length=10, blank=False, null=False, validators=[validate_amount],default='')
    ref1_person_name = models.CharField(max_length=200,default='', blank=False, null=False, validators=[validate_only_letters])
    ref2_person_name = models.CharField(max_length=200,default='', blank=False, null=False, validators=[validate_only_letters])
    ref1_mobile_number = models.CharField(max_length=10,default='', blank=False, null=False, validators=[validate_mobile_number])
    ref2_mobile_number = models.CharField(max_length=200,default='', blank=False, null=False ,validators=[validate_mobile_number])

    # Co-Applicant Details
    coapplicant_first_name = models.CharField(max_length=100, default='', validators=[validate_only_letters])
    coapplicant_last_name = models.CharField(max_length=100, default='', validators=[validate_only_letters])
    coapplicant_gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Other')
    coapplicant_age = models.IntegerField(validators=[validate_age])
    coapplicant_relationship = models.CharField(max_length=50, default='')
    coapplicant_mobile_number = models.CharField(max_length=10, default='', validators=[validate_mobile_number])
    coapplicant_email_id = models.EmailField(validators=[validate_email])
    coapplicant_occupation = models.CharField(max_length=100, default='', validators=[validate_only_letters])
    coapplicant_net_income_per_month = models.CharField(max_length=10, default='', validators=[validate_amount])
    random_number = models.CharField(max_length=10, blank=True,null=True)

    
    def save(self, *args, **kwargs):
        if not self.random_number:
          
            last_entry = CustomerProfile.objects.filter(random_number__startswith='SLNHOM').order_by('-random_number').first()
            
            if last_entry:
              
                last_number = int(last_entry.random_number[6:])  
                new_number = last_number + 1
            else:
                
                new_number = 1001
          

            self.random_number = f"SLNHOM{new_number:04d}"
        
        print(f"Saving CustomerProfile with random_number: {self.random_number}")
        super(CustomerProfile, self).save(*args, **kwargs)



    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class ApplicantDocument(models.Model):
    applicant_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, default=1)

   
    # Common fields
    adhar_card_front = models.ImageField(upload_to='documents/',null=False, blank=False,validators=[validate_image_file])
    adhar_card_back = models.ImageField(upload_to='documents/',null=False, blank=False,validators=[validate_image_file],default='')
    pan_card = models.ImageField(upload_to='documents/',null=False, blank=False,validators=[validate_image_file],default='')
    customer_photo = models.ImageField(upload_to='documents/',null=False, blank=False,validators=[validate_image_file],default='')
    home_plot_photo_1 = models.ImageField(upload_to='documents/',null=False, blank=False,validators=[validate_image_file],default='')
    home_plot_photo_2 = models.ImageField(upload_to='documents/',null=False, blank=False,validators=[validate_image_file],default='')
    home_plot_photo_3 = models.ImageField(upload_to='documents/',null=False, blank=False,validators=[validate_image_file],default='')
    home_plot_photo_4 = models.ImageField(upload_to='documents/,',null=False, blank=False,validators=[validate_image_file],default='')
    latest_3_months_banked_statement = models.FileField(upload_to='documents/',null=True, blank=True,validators=[validate_pdf_file])
    latest_3_months_payslips_1 = models.FileField(upload_to='documents/',null=True, blank=True,validators=[validate_pdf_file])
    latest_3_months_payslips_2 = models.FileField(upload_to='documents/',null=True, blank=True,validators=[validate_pdf_file])
    latest_3_months_payslips_3 = models.FileField(upload_to='documents/',null=True, blank=True,validators=[validate_pdf_file])
    employee_id_card = models.ImageField(upload_to='documents/',null=True, blank=True,validators=[validate_image_file])

    # HLBT fields
    business_proof_1 = models.FileField(upload_to='documents/', null=True, blank=True,validators=[validate_image_file])
    business_proof_2 = models.FileField(upload_to='documents/', blank=True, null=False,validators=[validate_image_file])
    latest_12_months_banked_statement = models.FileField(upload_to='documents/', blank=True, null=True,validators=[validate_pdf_file])
    business_office_photo = models.ImageField(upload_to='documents/', blank=True, null=True,validators=[validate_image_file])
    latest_3_yrs_itr_1 = models.FileField(upload_to='documents/', blank=True, null=True,validators=[validate_pdf_file])
    latest_3_yrs_itr_2 = models.FileField(upload_to='documents/', blank=True, null=True,validators=[validate_pdf_file])
    latest_3_yrs_itr_3 = models.FileField(upload_to='documents/', blank=True, null=True,validators=[validate_pdf_file])
    current_address_proof = models.FileField(upload_to='documents/', blank=True, null=True,validators=[validate_image_file])

    # Business fields
    existing_loan_statement = models.FileField(upload_to='documents/', blank=False, null=False,validators=[validate_pdf_file],default='')
    other_documents_1 = models.FileField(upload_to='documents/', blank=False, null=False,validators=[validate_pdf_file],default='')
    other_documents_2 = models.FileField(upload_to='documents/', blank=False, null=False,validators=[validate_pdf_file],default='')
    other_documents_3 = models.FileField(upload_to='documents/', blank=False, null=False,validators=[validate_pdf_file],default='')
    other_documents_4 = models.FileField(upload_to='documents/', blank=False, null=False,validators=[validate_pdf_file],default='')

    # Co-Applicant Details
    co_adhar_card_front = models.ImageField(upload_to='documents/', blank=False, null=False,validators=[validate_image_file])
    co_adhar_card_back = models.ImageField(upload_to='documents/', blank=False, null=False,validators=[validate_image_file])
    co_pan_card = models.ImageField(upload_to='documents/', blank=False, null=False,validators=[validate_image_file])
    co_selfie_photo = models.ImageField(upload_to='documents/', blank=False, null=False,validators=[validate_image_file])
    random_number = models.CharField(max_length=6, blank=True, null=True)


    def __str__(self):
        return f"{self.adhar_card_front}"


class HomeApplication(models.Model):
    applicant_profile = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    personal_detail_verification = models.CharField(max_length=50, blank=True, )
    documents_upload_status = models.CharField(max_length=50, blank=True)
    kyc_documents_verification_status = models.CharField(max_length=50, blank=True)
    filed_officer_visit_inspection_status = models.CharField(max_length=50, blank=True)
    eligibility_check_status = models.CharField(max_length=50, blank=True)
    application_fee_paid_status = models.CharField(max_length=50, blank=True)
    tele_verification_status = models.CharField(max_length=50, blank=True)
    bank_login_fee_paid_status = models.CharField(max_length=50, blank=True)
    bank_login_done_status = models.CharField(max_length=50, blank=True)
    credit_manager_visit_status = models.CharField(max_length=50, blank=True)
    bank_nbfc_soft_loan_sanction_letter_issued_status = models.CharField(max_length=50, blank=True)
    legal_technical_completed_status = models.CharField(max_length=50, blank=True)
    final_loan_sanctioned_status = models.CharField(max_length=50, blank=True)
    agreement_signatures_done_status = models.CharField(max_length=50, blank=True)
    enach_auto_debit_done_status = models.CharField(max_length=50, blank=True)
    disbursement_status = models.CharField(max_length=50, blank=True)
    post_documentation_mortgage_status = models.CharField(max_length=50, blank=True)
    cheque_issued_loan_amount_credited_status = models.CharField(max_length=50, blank=True)


    

    def __str__(self):
        return f"Applicant Document: {self.personal_detail_verification}"
    



