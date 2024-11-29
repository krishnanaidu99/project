# forms.py

# forms.py

from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.db.models import Q



class BusinessLoanForm(forms.ModelForm):
   

    class Meta:
        model = BusinessLoan
        fields = '__all__'
        exclude = ['application_id']
       
        widgets = {
            
            'date_of_birth': forms.DateInput(attrs={'type': 'date','max': '2023-12-31'}),
            'business_establishment_date': forms.DateInput(attrs={'type': 'date'}),
            'pan_card_number': forms.TextInput(attrs={'pattern': '[A-Z]{5}[0-9]{4}[A-Z]{1}'}),
            'mobile_number':forms.NumberInput(attrs={'pattern':'[0-9]'}),
            'aadhar_card_number':forms.NumberInput(),
            'ref_1_person_mobile_number':forms.NumberInput(),
            'ref_2_person_mobile_number':forms.NumberInput(),
            
            

        }
        
       
    

    
# Mobile Numbers Validation
    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        if BusinessLoan.objects.filter(mobile_number=mobile_number).exclude(id=self.instance_id).exists():
            raise forms.ValidationError("Mobile number already existsss.")
        if len(mobile_number)!=10:
            raise forms.ValidationError("Mobile NUmber Length should be in 10 Digits")
        return mobile_number
    
    def clean_ref_1_person_mobile_number(self):
        ref1_moobile_number=self.cleaned_data.get('ref_1_person_mobile_number')
        if len(ref1_moobile_number)!=10:
            raise forms.ValidationError("Mobile NUmber Length should be in 10 Digits")
        return ref1_moobile_number
    

    def clean_ref_1_person_mobile_number(self):
        ref1_moobile_number=self.cleaned_data.get('ref_1_person_mobile_number')
        if len(ref1_moobile_number)!=10:
            raise forms.ValidationError("Mobile Number Length should be in 10 Digits")
        return ref1_moobile_number
    


    def clean_ref_2_person_mobile_number(self):
     ref2_mobile_number=self.cleaned_data.get('ref_2_person_mobile_number')
     if len(ref2_mobile_number)!=10:
            raise forms.ValidationError("Mobile Number Length should be in 10 Digits")
     return ref2_mobile_number
    
    def clean_aadhar_card_number(self):
        aadhar_card_number=self.cleaned_data.get('aadhar_card_number')
        if len(aadhar_card_number)!=12:
            raise forms.ValidationError("Aadhar Number Length should be in 10 Digits")
        return aadhar_card_number
    
    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None) 
        super().__init__(*args, **kwargs)
      
        


    




    # Mobile Numbers Validation


    # def _init_(self,*args, **kwargs):
    #     super(BusinessLoanForm,self)._init_(*args, **kwargs)
    #     self.fields['gst_number'].required=True



from django.utils.translation import gettext_lazy as _

class BusinessLoanDocumentForm(forms.ModelForm):
    class Meta:
        model = BusinessLoanDocument
        fields = '__all__'
        exclude = ['loan']
        widgets={

          'business_proof_1': forms.FileInput(attrs={'accept': '.pdf'}),
          'business_proof_2': forms.FileInput(attrs={'accept': '.pdf'}),
          'latest_12_months_bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'latest_3_yrs_itr_1': forms.FileInput(attrs={'accept': '.pdf'}),
          'latest_3_yrs_itr_2': forms.FileInput(attrs={'accept': '.pdf'}),
          'latest_3_yrs_itr_3': forms.FileInput(attrs={'accept': '.pdf'}),
          'current_address_proof': forms.FileInput(attrs={'accept': '.pdf'}),
          'bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'other_document_1': forms.FileInput(attrs={'accept': '.pdf'}),
          'other_document_2': forms.FileInput(attrs={'accept': '.pdf'}),


          'aadhar_card_front': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'aadhar_card_back': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'pan_card': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'customer_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
         'business_office_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),



        #   'pay_slip_1': forms.FileInput(attrs={'accept': '.pdf'}),




        }
        labels = {
            'aadhar_card_front': 'Aadhar Card Front (JPEG/PNG)',
            'aadhar_card_back': 'Aadhar Card Back (JPEG/PNG)',
            'pan_card': 'PAN Card (JPEG/PNG)',
            'customer_photo': 'Customer Photo (JPEG/PNG)',
            'business_proof_1': 'Business Proof 1 (PDF)',
            'business_proof_2': 'Business Proof 2 (PDF)',
            'latest_12_months_bank_statement': 'Latest 12 Months Bank Statement (PDF)',
            'business_office_photo': 'Business Office Photo (JPEG/PNG)',
            'latest_3_yrs_itr_1': 'Latest 3 Years ITR 1 (PDF)',
            'latest_3_yrs_itr_2': 'Latest 3 Years ITR 2 (PDF)',
            'latest_3_yrs_itr_3': 'Latest 3 Years ITR 3 (PDF)',
            'current_address_proof': 'Current Address Proof (PDF)',
            'other_document_1': 'Other Document 1 (PDF)',
            'other_document_2': 'Other Document 2 (PDF)',
        }

    def clean_aadhar_card_front(self):
        file = self.cleaned_data.get('aadhar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png') :
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file

    def clean_aadhar_card_back(self):
        file = self.cleaned_data.get('aadhar_card_back', False)
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
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
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
    

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = '__all__'


class ApplicationVerifyForm(forms.ModelForm):
    class Meta:
        model=ApplicationVerification
        fields='__all__'
        exclude=['loan']

    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
       
        for field in self.fields:
            if not getattr(instance, field):
                setattr(instance, field, 'Rejected')
        
        if commit:
            instance.save()
        return instance

class busBasicDetailForm(forms.ModelForm):
    random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = busbasicdetailform
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
        recent_applications = busbasicdetailform.objects.filter(
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

        