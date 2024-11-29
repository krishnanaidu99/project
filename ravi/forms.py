from .models import *
from django.utils import timezone
from datetime import timedelta
from django import forms

class plBasicDetailForm(forms.ModelForm):
    random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = plbasicdetailform
        fields = '__all__'
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'loantype': forms.Select(attrs={'class': 'form-control'}),
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
            'loantype':{'required':'this field is required'},
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

     
        three_months_ago = timezone.now() - timedelta(days=90)
        recent_applications = plbasicdetailform.objects.filter(
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
    

class hlBasicDetailForm(forms.ModelForm):
    random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = hlbasicdetailform
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

     
        three_months_ago = timezone.now() - timedelta(days=90)
        recent_applications = plbasicdetailform.objects.filter(
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
class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        fields = '__all__'
        exclude=['random_number']
        widgets = {
             'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
             'job_joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['aadhar_card_front', 'aadhar_card_back', 'pan_card', 'customer_photo', 'payslip_1',
                  'payslip_2', 'payslip_3', 'bank_statement', 'employee_id_card', 'current_address_proof',
                  'other_document_1', 'other_document_2']
        widgets = {
            'aadhar_card_front': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'aadhar_card_back': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'pan_card': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'customer_photo': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'payslip_1': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'payslip_2': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'payslip_3': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'bank_statement': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'employee_id_card': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'current_address_proof': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'other_document_1': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
            'other_document_2': forms.ClearableFileInput(attrs={'accept': 'application/pdf'}),
        }
        labels = {
            'aadhar_card_front': 'Aadhar Card Front (Image)',
            'aadhar_card_back': 'Aadhar Card Back (Image)',
            'pan_card': 'PAN Card (Image)',
            'customer_photo': 'Customer Photo (Image)',
            'payslip_1': 'Payslip 1 (PDF)',
            'payslip_2': 'Payslip 2 (PDF)',
            'payslip_3': 'Payslip 3 (PDF)',
            'bank_statement': 'Bank Statement (PDF)',
            'employee_id_card': 'Employee ID Card (Image)',
            'current_address_proof': 'Current Address Proof (Image)',
            'other_document_1': 'Other Document 1 (PDF)',
            'other_document_2': 'Other Document 2 (PDF)',
}


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        exclude=['random_number']

        widgets = {
            'loan_type': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'marital_status': forms.Select(attrs={'class': 'form-control'}),
             'income_source': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'email_id': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'example@example.com'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control','placeholder': '1234567890'}),
            'aadhar_card_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'XXXXXXXXXXXX'}),
            'pan_card_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'XXXXXXXXXX'}),
            'current_address': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'current_address_pincode': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Pincode'}),
            'aadhar_address': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'aadhar_pincode': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Pincode'}),
            'running_emis_per_month': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'net_salary_per_month': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Company Name'}),
            'company_type': forms.Select(attrs={'class': 'form-control'}),
            'job_joining_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'job_location': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Job Location'}),
            'total_experience': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'work_email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'example@example.com'}),
            'office_address_pincode': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Pincode'}),
            'net_income_per_month': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'business_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Business Name'}),
            'business_type': forms.Select(attrs={'class': 'form-control'}),
            'business_establishment_date': forms.DateInput(attrs={'class': 'form-control','type': 'date'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-control','placeholder': 'GST Number'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Mother\'s Name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Father\'s Name'}),
            'nature_of_business': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'turnover_per_year': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'business_address_pincode': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Pincode'}),
            'house_plot_purchase_value': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'required_loan_amount': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'ref1_person_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'ref1_person_name'}),
            'ref2_person_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'ref2_person_name'}),
            'ref1_mobile_number': forms.TextInput(attrs={'class': 'form-control','placeholder': '1234567890'}),
            'ref2_mobile_number': forms.TextInput(attrs={'class': 'form-control','placeholder': '1234567890'}),
            'ref2_first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'coapplicant_first_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}),
            'coapplicant_last_name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}),
            'coapplicant_age': forms. NumberInput(attrs={'class': 'form-control','placeholder': 'Age'}),
            'coapplicant_gender': forms.Select(attrs={'class': 'form-control','class': 'form-control'}),
            'coapplicant_mobile_number': forms.TextInput(attrs={'class': 'form-control','placeholder': '1234567890'}),
            'coapplicant_email_id': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'example@example.com'}),
            'coapplicant_relationship': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Relationship'}),
            'coapplicant_net_income_per_month': forms.NumberInput(attrs={'class': 'form-control','placeholder': '0'}),
            'coapplicant_occupation': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Occupation'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, you can customize widget attributes here
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'form-control'})


class ApplicantDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicantDocument
        fields = '__all__'
        exclude = ['applicant_profile']
        widgets = {
            'adhar_card_front': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'adhar_card_back': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'pan_card': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'customer_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'home_plot_photo_4': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'latest_3_months_banked_statement': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_months_payslips_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_months_payslips_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_months_payslips_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'employee_id_card': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'business_proof_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'business_proof_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'latest_12_months_banked_statement': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'business_office_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'latest_3_yrs_itr_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_yrs_itr_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'latest_3_yrs_itr_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'current_address_proof': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'existing_loan_statement': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_1': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_2': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_3': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'other_documents_4': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'co_adhar_card_front': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'co_adhar_card_back': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'co_pan_card': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'co_selfie_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'random_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ApplicationVerificationForm(forms.ModelForm):
   
    class Meta:
        model=ApplicationVerification
        fields='__all__'
        exclude=['personal_detail']

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
       
        for field in self.fields:
            if not getattr(instance, field):
                setattr(instance, field, 'Rejected')
        
        if commit:
            instance.save()
        return instance
    
class HomeapplicationForm(forms.ModelForm):
   
    class Meta:
        model= HomeApplication
        fields='__all__'
        exclude=['applicant_profile']

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
       
        for field in self.fields:
            if not getattr(instance, field):
                setattr(instance, field, 'Rejected')
        
        if commit:
            instance.save()
        return instance
