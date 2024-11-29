from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

class EducationalLoanForm(forms.ModelForm):
    class Meta:
        model = Educationalloan
        fields = '__all__'
        exclude=['application_id']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mail_id': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile_number': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'}),
            'university_name': forms.TextInput(attrs={'class': 'form-control'}),
            'score_card': forms.ClearableFileInput(attrs={'class': 'form-control','accept': '.pdf'}),
            'GRE_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'IELTS_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'TOEFL_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'Duolingo_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'PTE_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'student_work_experience': forms.Textarea(attrs={'class': 'form-control'}),
            'cibil_score': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'loan_required': forms.NumberInput(attrs={'class': 'form-control'}),
            'backlogs': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'residence_location': forms.TextInput(attrs={'class': 'form-control'}),
            'permanent_location': forms.TextInput(attrs={'class': 'form-control'}),
            'co_applicant_type': forms.Select(attrs={'class': 'form-control'}),
            'co_applicant_parent_name': forms.TextInput(attrs={'class': 'form-control salaried-field'}),
            'co_applicant_company_name': forms.TextInput(attrs={'class': 'form-control salaried-field'}),
            'co_applicant_salaried_designation': forms.TextInput(attrs={'class': 'form-control salaried-field'}),
            'co_applicant_salaried_net_pay': forms.NumberInput(attrs={'class': 'form-control salaried-field','pattern':'[0-9]'}),
            'co_applicant_salaried_emis': forms.NumberInput(attrs={'class': 'form-control salaried-field','pattern':'[0-9]'}),
            'co_applicant_salaried_cibil_score': forms.NumberInput(attrs={'class': 'form-control salaried-field','pattern':'[0-9]'}),
            'co_applicant_self_employed_business_name': forms.TextInput(attrs={'class': 'form-control self-employed-field hidden'}),
            'co_applicant_self_employed_itr_mandatory': forms.Select(attrs={'class': 'form-control self-employed-field hidden'}),
            'co_pplicant_self_employed_itr_amount': forms.NumberInput(attrs={'class': 'form-control self-employed-field hidden','pattern':'[0-9]'}),
            'co_applicant_self_employed_business_licence': forms.FileInput(attrs={'class': 'form-control self-employed-field hidden','accept': '.pdf'}),
            'property_location': forms.TextInput(attrs={'class': 'form-control'}),
            'co_applicant_property_details': forms.Select(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'property_market_value': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'property_govt_value': forms.NumberInput(attrs={'class': 'form-control','pattern':'[0-9]'}),
            'property_local_government_body': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels={

           'score_card':'Score Card (PDF) ',
           'co_applicant_self_employed_business_licence':'Co Applicant self Employed Business Licence (PDF)',


        }
    def __init__(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None)
        super().__init__(*args, **kwargs)
        
        


    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        
        if Educationalloan.objects.filter(mobile_number=mobile_number).exclude(id=self.instance_id).exists():
            raise forms.ValidationError("Mobile number already existss.")
        if not int(mobile_number)>0 or len(mobile_number)!=10:
            raise forms.ValidationError("Mobile NUmber Length should be in 10 Digits")
        return mobile_number
    
    def _init_(self, *args, **kwargs):
        self.instance_id = kwargs.get('instance_id', None)
        kwargs.pop('instance_id', None)  
        super(EducationalLoanForm, self)._init_(*args, **kwargs)
       

    def clean_score_card(self):
        file = self.cleaned_data.get('score_card', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    



class DocumentsForm(forms.ModelForm):
    

    class Meta:
        model=Educationloan_document_upload
        fields='__all__'
        exclude = ['loan']
        widgets={
          'pay_slip_1': forms.FileInput(attrs={'accept': '.pdf'}),
          'pay_slip_2': forms.FileInput(attrs={'accept': '.pdf'}),
          'pay_slip_3': forms.FileInput(attrs={'accept': '.pdf'}),
          'bank_statement': forms.FileInput(attrs={'accept': '.pdf'}),
          'employee_id_card': forms.FileInput(attrs={'accept': '.pdf'}),
        #   'pay_slip_1': forms.FileInput(attrs={'accept': '.pdf'}),

        
          'aadhar_card_front': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'aadhar_card_back': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'pan_card': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
          'customer_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),
        #  'business_office_photo': forms.FileInput(attrs={ 'accept': 'image/jpeg, image/png'}),




        }
        labels = {
         'adhar_card_front': 'Aadhar Card Front (JPEG/PNG)',
         'adhar_card_back': 'Aadhar Card Back (JPEG/PNG)',
         'pan_card': 'Pan Card  (JPEG/PNG)',
         'customer_photo': 'Customer Photo (JPEG/PNG)',
         'pay_slip_1': 'Pay Slip 1 (PDF)',
         'pay_slip_2': 'Pay Slip 2 (PDF)',
         'pay_slip_3': 'Pay Slip 3 (PDF)',
         'bank_statement': 'Bank Statement (PDF)',
         'employee_id_card': 'Employee Id Card (PDF)',


     }
        
       
        

        


    def clean_adhar_card_front(self):
        file = self.cleaned_data.get('adhar_card_front', False)
        if file:
            if not file.name.endswith('.jpg') and not file.name.endswith('.jpeg') and not file.name.endswith('.png'):
                raise ValidationError(_('Only JPG/JPEG files are allowed.'), code='invalid')
        return file
    
    def clean_adhar_card_back(self):
        file = self.cleaned_data.get('adhar_card_back', False)
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
    
    def clean_pay_slip_1(self):
        file = self.cleaned_data.get('pay_slip_1', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    def clean_pay_slip_2(self):
        file = self.cleaned_data.get('pay_slip_2', False)
        if file:
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file
    
    def clean_pay_slip_3(self):
        file = self.cleaned_data.get('pay_slip_3', False)
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
            if not file.name.endswith('.pdf'):
                raise ValidationError(_('Only PDF files are allowed.'), code='invalid')
        return file




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
    

class eduBasicDetailForm(forms.ModelForm):
    random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = edubasicdetailform
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
        recent_applications = edubasicdetailform.objects.filter(
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






