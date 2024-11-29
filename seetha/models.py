from django.db import models
from decimal import Decimal
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

class carbasicdetailform(models.Model):
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

    

class CarLoan(models.Model):

    CAR_LOAN_TYPE_CHOICES = [
    ('NEW', 'New'),
    ('USED', 'Used')
    ]

    INCOME_SOURCE_CHOICES = [
        ('Job', 'Job'),
        ('Business', 'Business'),
    ]

    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('O', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]

    COMPANY_TYPE_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('government', 'Government'),
        ('self_employed', 'Self Employed'),
        ('other', 'Other')
    ]

    BUSINESS_TYPE_CHOICES = [
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Partnership', 'Partnership'),
        ('Private Limited Company', 'Private Limited Company'),
        ('Public Limited Company', 'Public Limited Company'),
        ('LLP', 'Limited Liability Partnership'),
        ('Others', 'Others'),
    ]

    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]

    # personal details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=10, unique=True)
    
    # car loan type
    car_loan_type = models.CharField(max_length=4, choices=CAR_LOAN_TYPE_CHOICES,null=True )
    
    # used car
    car_vehicle_no = models.CharField(max_length=15,null=True,blank=True)
    car_company_name = models.CharField(max_length=50,null=True,blank=True)
    variant = models.CharField(max_length=50, null=True,blank=True)
    model_year = models.IntegerField(blank=True, null=True)

    # new car
    car_purchase_value_in_RS = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    required_loan_amount1 = models.DecimalField(max_digits=15, decimal_places=2, null=True,blank=True)
    quotation_valaue_on_ex_showroom = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    downpayment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    showroom_quotation = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    # common fields    
    pan_card_number = models.CharField(max_length=10, unique=True)
    aadhar_card_number = models.CharField(max_length=12, unique=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    email_id = models.EmailField()
    current_address = models.TextField()
    current_address_pincode = models.IntegerField()
    aadhar_address = models.TextField()
    aadhar_pincode = models.IntegerField()
    running_emis_amount_per_month = models.DecimalField(max_digits=15, decimal_places=2)

    #income source
    income_source = models.CharField(max_length=10, choices=INCOME_SOURCE_CHOICES,default='')
    #job fields
    net_salary_per_month = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    company_name = models.CharField(max_length=100,null=True,blank=True)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPE_CHOICES,blank=True)
    job_designation = models.CharField(max_length=100,null=True,blank=True)
    job_joining_date = models.DateField(null=True,blank=True)
    job_location = models.CharField(max_length=100,null=True,blank=True)
    total_job_experience = models.CharField(max_length=50,null=True,blank=True)
    work_email = models.EmailField(null=True,blank=True)
    office_address = models.TextField(null=True,blank=True)

    #bussiness fiedls
    business_name = models.CharField(max_length=200,null=True,blank=True)
    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPE_CHOICES,null=True,blank=True)
    net_income_per_month = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    business_establishment_date = models.DateField(null=True,blank=True)
    gst_certificate = models.CharField(max_length=1, choices=YES_NO_CHOICES,null=True,blank=True)
    gst_number = models.CharField(max_length=15,null=True,blank=True)
    mother_name = models.CharField(max_length=100,null=True,blank=True)
    father_name = models.CharField(max_length=100,null=True,blank=True)
    nature_of_business = models.CharField(max_length=200,null=True,blank=True)
    turnover_in_lakhs_per_year = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    business_address = models.TextField(null=True,blank=True)
    business_address_pincode = models.IntegerField(null=True,blank=True)
    existing_loan_amount =models.DecimalField(max_digits=10,decimal_places=2, null=True,blank=True)
    required_loan_amount2 = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    ref_1_person_name = models.CharField(max_length=100,null=True,blank=True)
    ref_1_person_mobile_number = models.CharField(max_length=10,null=True,blank=True)
    ref_2_person_name = models.CharField(max_length=100,null=True,blank=True)
    ref_2_person_mobile_number = models.CharField(max_length=10,null=True,blank=True)
    own_house = models.CharField(max_length=1, choices=YES_NO_CHOICES,null=True,blank=True)
    remarks = models.TextField(null=True,blank=True)
    application_id=models.CharField(max_length=200,unique=True,null=True,blank=True)

    def __str__(self):
        return f"{self.id}={self.first_name} {self.last_name}"
    

    def save(self,*args,**kwargs):
        
        if not self.id:
            
            max_id = CarLoan.objects.aggregate(models.Max('id'))['id__max']
            if max_id is None:
                self.id = 1001
                self.application_id=f"SLNCAR{self.id}"
            else:
                all_ids = set(CarLoan.objects.values_list('id', flat=True))
                for i in range(1001, max_id + 2):
                    if i not in all_ids:
                        self.id = i
                        self.application_id=f"SLNCAR{self.id}"
                        break
        super(CarLoan,self).save(*args, **kwargs)


class CarLoanDocument(models.Model):
    loan = models.OneToOneField(CarLoan, on_delete=models.CASCADE, related_name='CarLoandocuments',blank=True)
    car_rc_front = models.ImageField(upload_to='documents/',null=True,blank=True)
    car_rc_back = models.ImageField(upload_to='documents/',null=True,blank=True)
    aadhaar_card_front = models.ImageField(upload_to='documents/')
    aadhaar_card_back = models.ImageField(upload_to='documents/')
    pan_card = models.ImageField(upload_to='documents/')
    customer_photo = models.ImageField(upload_to='documents/')
    #job documents
    payslip1 = models.FileField(upload_to='documents/',null=True,blank=True)
    payslip2 = models.FileField(upload_to='documents/',null=True,blank=True)
    payslip3 = models.FileField(upload_to='documents/',null=True,blank=True)
    bank_statement = models.FileField(upload_to='documents/',null=True,blank=True)
    employee_id_card = models.ImageField(upload_to='documents/',null=True,blank=True)
    #business documents
    business_proof_1 = models.FileField(upload_to='documents/',null=True,blank=True)
    business_proof_2 = models.FileField(upload_to='documents/',null=True,blank=True)
    latest_12_months_bank_statement = models.FileField(upload_to='documents/',null=True,blank=True)
    business_office_photo = models.FileField(upload_to='documents/',null=True,blank=True)
    latest_3_yrs_itr_1 = models.FileField(upload_to='documents/',null=True,blank=True)
    latest_3_yrs_itr_2 = models.FileField(upload_to='documents/',null=True,blank=True)
    latest_3_yrs_itr_3 = models.FileField(upload_to='documents/',null=True,blank=True)
    current_address_proof = models.FileField(upload_to='documents/',null=True,blank=True)
    existing_loan_statement = models.FileField(upload_to='documents/',null=True,blank=True)
    other_document_1 = models.FileField(upload_to='documents/',null=True,blank=True)
    other_document_2 = models.FileField(upload_to='documents/',null=True,blank=True)
    


    def __str__(self):
        return f"Documents for {self.loan.id}"
