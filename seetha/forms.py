from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.db.models import Q
# from decimal import Decimal
import re

from .models import CarLoan

class CarLoanForm(forms.ModelForm):
    # random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = CarLoan
        fields = '__all__'
        exclude=['application_id']
        
        widgets = {
            
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number':forms.NumberInput(attrs={'class': 'form-control','pattern': r'^\d{10}$',}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'car_loan_type': forms.Select(attrs={'id': 'id_car_loan_type'}),
            'income_source': forms.Select(attrs={'id': 'id_income_source'}),
            'car_vehicle_no': forms.TextInput(attrs={'pattern': r'^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{4}$'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'work_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'job_joining_date': forms.DateInput(attrs={'type': 'date'}),
            'total_job_experience': forms.NumberInput(attrs={'pattern': r'^\d{2}$'}),
            'business_establishment_date': forms.DateInput(attrs={'type': 'date'}),
            'pan_card_number': forms.TextInput(attrs={ 'pattern': r'^[A-Z]{5}\d{4}[A-Z]$'}),
            'aadhar_card_number':forms.NumberInput(),
            'current_address': forms.Textarea(attrs={'class': 'form-control'}),
            'aadhar_address': forms.Textarea(attrs={'class': 'form-control'}),
            'aadhar_pincode': forms.NumberInput(attrs={'pattern': r'^\d{6}$'}),
            'current_address_pincode': forms.NumberInput(attrs={'pattern': r'^\d{6}$'}),
            'net_salary_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_address_pincode': forms.NumberInput(attrs={'pattern': r'^\d{6}$'}),
            'net_income_per_month': forms.NumberInput(attrs={'class': 'form-control'}),
            'gst_certificate': forms.Select(attrs={'id': 'id_gst_certificate'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control'}),
            'existing_loan': forms.NumberInput(attrs={'class': 'form-control'}),
            'ref1_person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ref_1_person_mobile_number':forms.NumberInput(attrs={'pattern': r'^\d{10}$'}),
            'ref2_person_name': forms.TextInput(),
            'ref_2_person_mobile_number':forms.NumberInput(attrs={'pattern': r'^\d{10}$'}),
            'quotation_valaue_on_ex_showroom': forms.NumberInput(attrs={'class': 'form-control'}),
            'downpayment_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'showroom_quotation': forms.NumberInput(attrs={'class': 'form-control'}),
        }




    def _init_(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None) 
        super(CarLoanForm, self)._init_(*args, **kwargs)

    def clean_aadhar_card_number(self):
        aadhar = self.cleaned_data.get('aadhar_card_number')
        if not aadhar.isdigit():
            raise forms.ValidationError("Aadhaar number must contain only digits.")
        if len(aadhar) != 12:
            raise forms.ValidationError("Aadhaar number must be exactly 12 digits long.")
        return aadhar

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if mobile_number:
            mobile_number_str = str(mobile_number)
            if not re.match(r'^\d{10}$', mobile_number_str):
                raise forms.ValidationError("Mobile number must be exactly 10 digits.")
        return mobile_number

    def clean_email_id(self):
        email = self.cleaned_data.get('email_id')
        if email and not re.match(r'^[a-zA-Z]', email):
            raise ValidationError("Email must start with an alphabet.")
        return email
    
    
    def clean_work_email(self):
        work_email = self.cleaned_data.get('work_email')
        if work_email and not re.match(r'^[a-zA-Z]', work_email):
            raise ValidationError("Work email must start with an alphabet.")

        return work_email
    
    
    def clean_gst_number(self):
        gst_number = self.cleaned_data.get('gst_number')
        if gst_number and not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$', gst_number):
            raise ValidationError("Invalid GST number format.")
    
        return gst_number

   
    
    def clean_ref_1_person_mobile_number(self):
        ref_1_mobile = self.cleaned_data.get('ref_1_person_mobile_number')
        if ref_1_mobile:
            if len(ref_1_mobile) != 10 or not ref_1_mobile.isdigit():
                raise forms.ValidationError("Reference 1 mobile number must be exactly 10 digits.")
        return ref_1_mobile

    def clean_ref_2_person_mobile_number(self):
        ref_2_mobile = self.cleaned_data.get('ref_2_person_mobile_number')
        if ref_2_mobile:
            if len(ref_2_mobile) != 10 or not ref_2_mobile.isdigit():
                raise forms.ValidationError("Reference 2 mobile number must be exactly 10 digits.")
        return ref_2_mobile
    

    def clean_pan_card(self):
        pan_card = self.cleaned_data.get('pan_card')
        if pan_card and not re.match(r'^[A-Z]{5}\d{4}[A-Z]$', pan_card):
            raise forms.ValidationError("PAN card number must be in the correct format (e.g., ABCDE1234F).")
        return pan_card
    
    def clean_total_job_experience(self):
        total_job_experience = self.cleaned_data.get('total_job_experience')
        if total_job_experience is not None:
            total_job_experience_str = str(total_job_experience).zfill(2)
            if not re.match(r'^\d{2}$', total_job_experience_str):
                raise forms.ValidationError("Total job experience must be exactly 2 digits.")
        return total_job_experience
    
    def clean_model_year(self):
        model_year = self.cleaned_data.get('model_year')
        if model_year:
            model_year_str = str(model_year)
            if not re.match(r'^\d{4}$', model_year_str):
                raise forms.ValidationError("Model year must be a 4-digit number.")
        return model_year

    

    def clean_car_vehicle_no(self):
        vehicle_no = self.cleaned_data.get('car_vehicle_no')
        if vehicle_no and not re.match(r'^[A-Z]{2}\d{1,2}[A-Z]{1,2}\d{4}$', vehicle_no):
            raise forms.ValidationError("Car vehicle number must be in the correct format (e.g., MH12AB1234 or KA01C5678).")
        return vehicle_no
    
   
    
    def validate_aadhar_pincode(pincode):
        if len(str(pincode)) != 6 or not str(pincode).isdigit():
           raise ValidationError('Pincode must be exactly 6 digits.')

    def clean_current_address_pincode(self):
        current_address_pincode = self.cleaned_data.get('current_address_pincode')
        if current_address_pincode:
            current_address_pincode_str = str(current_address_pincode)
            if not re.match(r'^\d{6}$', current_address_pincode_str):
                raise forms.ValidationError("Current address pincode must be a 6-digit number.")
        return current_address_pincode
    
    def clean_business_address_pincode(self):
        business_address_pincode = self.cleaned_data.get('current_address_pincode')
        if business_address_pincode:
            current_address_pincode_str = str(business_address_pincode)
            if not re.match(r'^\d{6}$', current_address_pincode_str):
                raise forms.ValidationError("Current address pincode must be a 6-digit number.")
        return business_address_pincode


from django.utils.translation import gettext_lazy as _

class CarLoanDocumentForm(forms.ModelForm):
    class Meta:
        model = CarLoanDocument
        fields = '__all__'
        exclude = ['loan']
        labels = {
            
            'car_rc_front': 'Car Rc Front(JPEG)',
            'car_rc_back': 'Car Rc Back (JPEG)',
            'aadhaar_card_front': 'Aadhar Card Front (JPEG)',
            'aadhaar_card_back': 'Aadhar Card Back (JPEG)',
            'pan_card': 'PAN Card (JPEG)',
            'customer_photo': 'Customer Photo (JPEG)',
            'payslip1': 'Payslip 1 (PDF)',
            'payslip2': 'Payslip 2 (PDF)',
            'payslip3': 'Payslip 3 (PDF)',
            'bank_statement': 'Bank Statement (PDF)',
            'employee_id_card': 'Employee ID Card (JPEG)',
            'business_proof_1': 'Business Proof 1 (PDF)',
            'business_proof_2': 'Business Proof 2 (PDF)',
            'latest_12_months_bank_statement': 'Latest 12 Months Bank Statement (PDF)',
            'business_office_photo': 'Business Office Photo (JPEG)',
            'latest_3_yrs_itr_1': 'Latest 3 Years ITR 1 (PDF)',
            'latest_3_yrs_itr_2': 'Latest 3 Years ITR 2 (PDF)',
            'latest_3_yrs_itr_3': 'Latest 3 Years ITR 3 (PDF)',
            'current_address_proof': 'Current Address Proof (PDF)',
            'existing_loan_statement': 'Existing Loan Statement (PDF)',
            'other_document_1': 'Other Document 1 (PDF)',
            'other_document_2': 'Other Document 2 (PDF)',
            
        }


    def clean_car_rc_front(self):
        file = self.cleaned_data.get('car_rc_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG/PNG files are allowed.'), code='invalid')
        return file

    def clean_car_rc_back(self):
        file = self.cleaned_data.get('car_rc_back', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG/PNG files are allowed.'), code='invalid')
        return file
    
    def clean_aadhaar_card_front(self):
        file = self.cleaned_data.get('aadhaar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file
    
    def clean_aadhaar_card_back(self):
        file = self.cleaned_data.get('aadhaar_card_back', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_pan_card(self):
        file = self.cleaned_data.get('pan_card', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_customer_photo(self):
        file = self.cleaned_data.get('customer_photo', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file
    
    def clean_payslip1(self):
        file = self.cleaned_data.get('payslip1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_payslip2(self):
        file = self.cleaned_data.get('payslip2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_payslip3(self):
        file = self.cleaned_data.get('payslip3', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    def clean_bank_statement(self):
        file = self.cleaned_data.get('bank_statement', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    def clean_employee_id_card(self):
        file = self.cleaned_data.get('employee_id_card', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') or file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG/PNG files are allowed.'), code='invalid')
        return file

    def clean_business_proof_1(self):
        file = self.cleaned_data.get('business_proof_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_business_proof_2(self):
        file = self.cleaned_data.get('business_proof_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_latest_12_months_bank_statement(self):
        file = self.cleaned_data.get('latest_12_months_bank_statement', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_business_office_photo(self):
        file = self.cleaned_data.get('business_office_photo', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_latest_3_yrs_itr_1(self):
        file = self.cleaned_data.get('latest_3_yrs_itr_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_latest_3_yrs_itr_2(self):
        file = self.cleaned_data.get('latest_3_yrs_itr_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_latest_3_yrs_itr_3(self):
        file = self.cleaned_data.get('latest_3_yrs_itr_3', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_current_address_proof(self):
        file = self.cleaned_data.get('current_address_proof', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    def clean_existing_loan_statement(self):
        file = self.cleaned_data.get('existing_loan_statement', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_other_document_1(self):
        file = self.cleaned_data.get('other_document_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file

    def clean_other_document_2(self):
        file = self.cleaned_data.get('other_document_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file


class carBasicDetailForm(forms.ModelForm):
    random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = carbasicdetailform
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pan_number': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
            'required_loan_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'terms_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'random_number': forms.HiddenInput(),
        }
        error_messages = {
            'full_name': {'required': 'Full name is required.'},
            'pan_number': {'required': 'Pan number is required.'},
            'gender': {'required': 'Gender is required.'},
            'email': {'required': 'Email is required.'},
            'date_of_birth': {'required': 'Date of birth is required.'},
            'marital_status': {'required': 'Marital status is required.'},
            'required_loan_amount': {'required': 'Required loan amount is required.'},
            'terms_accepted': {'required': 'You must accept the terms and conditions to proceed.'},
        }

    def clean(self):
        cleaned_data = super().clean()
        pan_number = cleaned_data.get('pan_number')

        # Check for previous applications within the last three months
        three_months_ago = timezone.now() - timedelta(days=90)
        recent_applications = carbasicdetailform.objects.filter(
            pan_number=pan_number,
            created_at__gte=three_months_ago
        ).order_by('-created_at')

        if recent_applications.exists():
            most_recent_application = recent_applications.first()
            reapply_date = most_recent_application.created_at + timedelta(days=90)
            error_message = f"You have already applied within the last three months. Please reapply after {reapply_date.strftime('%Y-%m-%d')}."
            raise forms.ValidationError(error_message)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
        return instance
       

