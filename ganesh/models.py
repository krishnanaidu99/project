from django.db import models
from django.core.validators import EmailValidator
import random
import string
import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Max


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
    

def validate_accountnumber(value):
    pattern = r'^\d{}$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid account nymber format')
    
    
    

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
                raise ValidationError(('Only JPG/JPEG files are allowed.'), code='invalid')
        return file
def clean_business_proof_1(self):
        file = self.cleaned_data.get('business_proof_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(('Only PDF files are allowed.'), code='invalid')
        return file
def validate_image_file(value):
    if not (value.name.endswith('.jpg') or value.name.endswith('.png') or value.name.endswith('.jpeg')):
        raise ValidationError('Only JPG/JPEG files are allowed.')


def validate_pdf_file(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')
def validate_date(value):
    if value > timezone.now().date():
        raise ValidationError('Date cannot be in the future.')

class CreditCardApplication(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ('Employed', 'Employed'),
        ('Self-Employed', 'Self-Employed'),
        ('Unemployed', 'Unemployed'),
        ('Student', 'Student'),
        ('Retired', 'Retired'),
    ]

    ACCOUNT_TYPE_CHOICES = [
        ('Current', 'Current'),
        ('Savings', 'Savings'),
    ]

    CARD_TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Rewards', 'Rewards'),
        ('Travel', 'Travel'),
        ('Cashback', 'Cashback'),
        ('Business', 'Business'),
    ]

    PURPOSE_CHOICES = [
        ('Travel', 'Travel'),
        ('Business', 'Business'),
        ('Everyday Use', 'Everyday Use'),
        ('Other', 'Other'),
    ]

    condition_CHOICES = [
        ('YES', 'yes'),
        ('NO', 'no'),
    ]

    full_name = models.CharField(max_length=100, null=False,blank=False,validators=[validate_only_letters],default="a")
    date_of_birth = models.DateField(validators=[validate_date])
    gender = models.CharField(max_length=10,help_text="select", choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=50, null=True,validators=[validate_only_letters])

    # Address Details
    current_street_address = models.CharField(max_length=255,null=False,blank=False,default="a")
    current_city = models.CharField(max_length=100,validators=[validate_only_letters],null=False,blank=False)
    current_state_province = models.CharField(max_length=100,validators=[validate_only_letters],null=False,blank=False)
    current_postal_code = models.CharField(max_length=6,null=True, blank=True,validators=[validate_pincode])  # Changed to CharField
    
    current_country = models.CharField(max_length=50, null=True, blank=True,validators=[validate_only_letters])

    permanent_street_address = models.CharField(max_length=255,null=False,blank=False,default="a")
    permanent_city = models.CharField(max_length=100,null=False,blank=False,validators=[validate_only_letters],default="a")
    permanent_state_province = models.CharField(max_length=100, null=True, blank=True,validators=[validate_only_letters])
    permanent_postal_code = models.CharField(max_length=6,null=True, blank=True,validators=[validate_pincode]) 
    
     
    permanent_country = models.CharField(max_length=50,null=True, blank=True,validators=[validate_only_letters])

    phone_number = models.CharField(max_length=10,null=True,validators=[validate_mobile_number])
    email_address = models.EmailField(validators=[validate_email])



    # Employment Information
    employment_status = models.CharField(max_length=15, choices=EMPLOYMENT_STATUS_CHOICES, null=False,default="a")
    occupation = models.CharField(max_length=100, blank=True,validators=[validate_only_letters])
    employer_name = models.CharField(max_length=100, blank=True,validators=[validate_only_letters])
    employer_address = models.CharField(max_length=255, blank=True)
    work_phone_number = models.CharField(max_length=10,null=True,validators=[validate_mobile_number])  # Changed to CharField
    years_at_current_job = models.CharField(blank=True, null=True,max_length=2)
    monthly_annual_income = models.CharField(max_length=15, blank=True, null=True,validators=[validate_amount])

    # Financial Information
    bank_name = models.CharField(max_length=100, blank=True,validators=[validate_only_letters])
    account_number = models.CharField(null=True, blank=True,max_length=20) # Changed to CharField
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, blank=True)
    monthly_housing_payment = models.CharField(max_length=10, blank=True, null=True,validators=[validate_amount])
    other_monthly_obligations = models.CharField(max_length=10, blank=True, null=True,validators=[validate_amount])
    total_monthly_expenses = models.IntegerField(blank=True, null=True,validators=[validate_amount])

    # Credit Information
    existing_credit_cards = models.CharField(blank=True, null=True,max_length=1)  # You may consider JSONField if structured data is needed
    other_debts_loans = models.CharField(blank=True,max_length=2)

    # Additional Information
    preferred_credit_card_type = models.CharField(max_length=10, choices=CARD_TYPE_CHOICES, blank=True,validators=[validate_only_letters],default='select')
    purpose_of_credit_card = models.CharField(max_length=15, choices=PURPOSE_CHOICES, blank=True)
    referral_code = models.CharField(max_length=5, blank=True,null=True)

    # Legal Agreements
    terms_and_conditions_agreed = models.CharField(max_length=10,choices=condition_CHOICES)
    privacy_policy_agreed = models.CharField(max_length=10,choices=condition_CHOICES,help_text='select')
    electronic_signature = models.FileField(upload_to='proof_of_income/',
                                       help_text='Upload proof of income such as payslips or tax returns.',validators=[validate_pdf_file])
    
    random_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.random_number:
            # Query to get the last number with the prefix 'SLNLAP-'
            last_entry = CreditCardApplication.objects.filter(random_number__startswith='SLNCC-').aggregate(Max('random_number'))
            last_number = last_entry['random_number__max']

            if last_number:
                # Extract the number part, increment it, and format the new number
                last_number_int = int(last_number.split('-')[1])  # Split on hyphen and extract number
                new_number = last_number_int + 1
            else:
                # Starting number if no entries exist
                new_number = 1001

            # Set the new random_number with hyphen and zero-padding
            self.random_number = f"SLNCC-{new_number:04d}"
        
        print(f"Saving LoanApplication with random_number: {self.random_number}")
        super(CreditCardApplication, self).save(*args, **kwargs)

 
    def _str_(self):
        return f"{self.full_name} - {self.email_address}"
    















class CreditDocumentUpload(models.Model):
    personal_details = models.ForeignKey(CreditCardApplication, on_delete=models.CASCADE)

    proof_of_identity = models.FileField(upload_to='proof_of_identity/', blank=False, null=False,
                                         help_text='Upload proof of identity such as a passport or driver’s license.',validators=[validate_pdf_file])
    proof_of_address = models.FileField(upload_to='proof_of_address/', blank=False, null=False,
                                        help_text='Upload proof of address such as a utility bill or lease agreement.',validators=[validate_pdf_file])
    proof_of_income = models.FileField(upload_to='proof_of_income/', blank=False, null=False,
                                       help_text='Upload proof of income such as payslips or tax returns.',validators=[validate_pdf_file])

    def _str_(self):
        return f"Documents for {self.proof_of_address}-{self.proof_of_income}"











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

from datetime import date
def validate_age(date_of_birth):
    if not isinstance(date_of_birth, date):
        raise ValidationError('Invalid date format.')
    
    today = date.today()
    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    
    if not (18 <= age <= 70):
        raise ValidationError('Age must be between 18 and 70 years.')
    


class crebasicdetailform(models.Model):
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

    
   




