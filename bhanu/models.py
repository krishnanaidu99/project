from django.db import models
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

# Create your models here.

class Educationalloan(models.Model):
    APPLICANT_TYPE_CHOICES = [
        ('SALARIEDEMPLOYEE', 'Salariedemployee'),
        ('SELFEMPLOYEED', 'SelfEmployeed'),
    ]

    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]


    student_name = models.CharField(max_length=100)
    mail_id = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=10, unique=True)
    country = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)
    score_card = models.FileField(upload_to='score_cards/')
    
    GRE_score = models.DecimalField(max_digits=15, decimal_places=2)
    IELTS_score = models.DecimalField(max_digits=15, decimal_places=2)
    TOEFL_score = models.DecimalField(max_digits=15, decimal_places=2)
    Duolingo_score = models.DecimalField(max_digits=15, decimal_places=2)
    PTE_score = models.DecimalField(max_digits=15, decimal_places=2)
    
    student_work_experience = models.TextField()
    cibil_score = models.IntegerField()
    loan_required = models.DecimalField(max_digits=15, decimal_places=2)
    backlogs = models.PositiveIntegerField()

    residence_location = models.CharField(max_length=200)
    permanent_location = models.CharField(max_length=200)

    co_applicant_type = models.CharField(max_length=20, choices=APPLICANT_TYPE_CHOICES)

    co_applicant_parent_name = models.CharField(max_length=100,null=True,blank=True)
    co_applicant_company_name = models.CharField(max_length=100, null=True,blank=True)
    co_applicant_salaried_designation = models.CharField(max_length=100, null=True,blank=True)
    co_applicant_salaried_net_pay = models.DecimalField(max_digits=15, decimal_places=2, null=True,blank=True)
    co_applicant_salaried_emis = models.DecimalField(max_digits=15, decimal_places=2, null=True,blank=True)
    co_applicant_salaried_cibil_score = models.IntegerField(null=True,blank=True)

    co_applicant_self_employed_business_name = models.CharField(max_length=100, null=True,blank=True)
    co_applicant_self_employed_itr_mandatory = models.CharField(max_length=1, choices=YES_NO_CHOICES,null=True,blank=True)
    co_pplicant_self_employed_itr_amount = models.DecimalField(max_digits=15, decimal_places=2,null=True,blank=True)
    co_applicant_self_employed_business_licence = models.FileField(upload_to='business_licences/', null=True,blank=True)

   
    property_location = models.CharField(max_length=200)
    co_applicant_property_details = models.CharField(max_length=1, choices=YES_NO_CHOICES)
    property_type = models.CharField(max_length=50, choices=[('House', 'House'), ('Plot', 'Plot'), ('Flat', 'Flat'), ('Apartment', 'Apartment'), ('Open Land', 'Open Land')])
    property_market_value = models.DecimalField(max_digits=15, decimal_places=2)
    property_govt_value = models.DecimalField(max_digits=15, decimal_places=2)
    property_local_government_body = models.CharField(max_length=100)
    application_id=models.CharField(max_length=200,unique=True,blank=True)

    def __str__(self):
        return f"{self.id}---{self.student_name}"
    

    def save(self,*args,**kwargs):
        
        if not self.id:
            
            max_id = Educationalloan.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 1001
                self.application_id=f"SLNEDU{self.id}"
            else:
                all_ids = set(Educationalloan.objects.values_list('id', flat=True))
                for i in range(1001, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        self.application_id=f"SLNEDU{self.id}"
                        break
        super(Educationalloan,self).save(*args, **kwargs)
    
   




class Educationloan_document_upload(models.Model):
        loan = models.OneToOneField(Educationalloan, on_delete=models.CASCADE, related_name='personal_details')
        

        adhar_card_front = models.ImageField(
        upload_to='EDUdocuments/adhar_card/front/',
        
    )
        adhar_card_back = models.ImageField(
        upload_to='EDUdocuments/adhar_card/back/',
       
        
    )
        pan_card = models.ImageField(
        upload_to='EDUdocuments/pan_card/',

       
    )
        customer_photo = models.ImageField(
        upload_to='EDUdocuments/customer_photo/',
        
        
    )
        pay_slip_1 = models.FileField(
        upload_to='EDUdocuments/pay_slips/',
       
    )
        pay_slip_2 = models.FileField(
        upload_to='EDUdocuments/pay_slips/',
       
    )
        pay_slip_3 = models.FileField(
        upload_to='EDUdocuments/pay_slips/',
       
    )
        bank_statement = models.FileField(
        upload_to='EDUdocuments/bank_statements/',
       
    )
        employee_id_card = models.FileField(
        upload_to='EDUdocuments/employee_id_cards/',
       
    )

        def __str__(self):
         return f"{self.employee_id_card}"





class ApplicationVerification(models.Model):

    loan= models.OneToOneField(Educationalloan, on_delete=models.CASCADE, related_name='applicationverification',blank=True)
    personal_detail_verifaction=models.CharField(max_length=50,blank=True)
    documents_upload_verification=models.CharField(max_length=50,blank=True)
    documents_verification=models.CharField(max_length=50,blank=True)
    eligibility_check_verification=models.CharField(max_length=50,blank=True)
    bank_login_verification=models.CharField(max_length=50,blank=True)
    kyc_and_document_verification=models.CharField(max_length=50,blank=True)
    enach_verification=models.CharField(max_length=50,blank=True)
    field_verification=models.CharField(max_length=50,blank=True)
    income_verification=models.CharField(max_length=50,blank=True)
    verification_status=models.CharField(max_length=100,blank=True)


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

def validate_aadhar_number(value):
      # Convert the value to a string
    if len(value) != 12 or not value.isdigit():
        raise ValidationError('Invalid Aadhar number format. It should be exactly 12 digits and contain only numbers.')

def validate_pincode(value):
    pattern = r'^\d{6}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid pincode format')



def validate_amount(value):
    if len(str(value)) > 10:
        raise ValidationError('Amount must be lessthan 10 digits.')
    
def validate_date(value):
    if value  > timezone.now().date():
        raise ValidationError('Date should be in past or present')
    
def validate_gst_number(value):
    gst_regex = re.compile(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$')
    
    value_str = str(value)  # Convert the value to a string
    if not gst_regex.match(value_str):
        raise ValidationError('Invalid GST number format.')

def validate_age(value):
    # Ensure value is an integer and within the expected range
    if not (18 <= value <= 70):
        raise ValidationError('Apply between 18 and 70')

class edubasicdetailform(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female')]
    MARITAL_STATUS_CHOICES = [('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced')]
    
    full_name = models.CharField(max_length=25,validators=[validate_only_letters])
    pan_number = models.CharField(max_length=10, validators=[validate_pan])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    email = models.EmailField(validators=[EmailValidator()])
    date_of_birth = models.DateField(validators=[validate_date])
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, default='Single')
    required_loan_amount = models.DecimalField(max_digits=50, decimal_places=2,validators=[validate_amount])
    terms_accepted = models.BooleanField(default=False,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    random_number = models.CharField(max_length=6, blank=True)

    def __str__(self):
        return f"{self.full_name}"

    