from django import forms
from .models import *

from django.utils import timezone
from datetime import timedelta

class CreditCardApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditCardApplication
        fields = '__all__'
        exclude=['random_number']
        widgets = {
           'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
 
    #     'full_name': forms.TextInput(attrs={'class': 'form-control'}),
    #     'gender': forms.Select(choices=CreditCardApplication.GENDER_CHOICES, attrs={'class': 'form-control'}),
    #     'marital_status': forms.Select(choices=CreditCardApplication.MARITAL_STATUS_CHOICES, attrs={'class': 'form-control'}),
    #     'nationality': forms.TextInput(attrs={'class': 'form-control'}),
    #     'current_street_address': forms.TextInput(attrs={'class': 'form-control'}),
    #     'current_city': forms.TextInput(attrs={'class': 'form-control'}),
    #     'current_state_province': forms.TextInput(attrs={'class': 'form-control'}),
    #     'current_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
    #     'current_country': forms.TextInput(attrs={'class': 'form-control'}),
    #     'permanent_street_address': forms.TextInput(attrs={'class': 'form-control'}),
    #     'permanent_city': forms.TextInput(attrs={'class': 'form-control'}),
    #     'permanent_state_province': forms.TextInput(attrs={'class': 'form-control'}),
    #     'permanent_postal_code': forms.TextInput(attrs={'class': 'form-control'}),
    #     'permanent_country': forms.TextInput(attrs={'class': 'form-control'}),
    #     'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
    #     'email_address': forms.EmailInput(attrs={'class': 'form-control'}),
    #     'employment_status': forms.Select(choices=CreditCardApplication.EMPLOYMENT_STATUS_CHOICES, attrs={'class': 'form-control'}),
    #     'occupation': forms.TextInput(attrs={'class': 'form-control'}),
    #     'employer_name': forms.TextInput(attrs={'class': 'form-control'}),
    #     'employer_address': forms.TextInput(attrs={'class': 'form-control'}),
    #     'work_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
    #     'years_at_current_job': forms.NumberInput(attrs={'class': 'form-control'}),
    #     'monthly_annual_income': forms.NumberInput(attrs={'class': 'form-control'}),
    #     'bank_name': forms.TextInput(attrs={'class': 'form-control'}),
    #     'account_number': forms.TextInput(attrs={'class': 'form-control'}),
    #     'account_type': forms.Select(choices=CreditCardApplication.ACCOUNT_TYPE_CHOICES, attrs={'class': 'form-control'}),
    #     'monthly_housing_payment': forms.NumberInput(attrs={'class': 'form-control'}),
    #     'other_monthly_obligations': forms.NumberInput(attrs={'class': 'form-control'}),
    #     'total_monthly_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
    #     'existing_credit_cards': forms.TextInput(attrs={'class': 'form-control'}),
    #     'other_debts_loans': forms.TextInput(attrs={'class': 'form-control'}),
    #     'preferred_credit_card_type': forms.Select(choices=CreditCardApplication.CARD_TYPE_CHOICES, attrs={'class': 'form-control'}),
    #     'purpose_of_credit_card': forms.Select(choices=CreditCardApplication.PURPOSE_CHOICES, attrs={'class': 'form-control'}),
    #     'referral_code': forms.TextInput(attrs={'class': 'form-control'}),
    #     'terms_and_conditions_agreed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    #     'privacy_policy_agreed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    #     'electronic_signature': forms.TextInput(attrs={'class': 'form-control'}),
    # }

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = CreditDocumentUpload
        fields = '__all__'
        exclude=['personal_details']


       
 
       

class creBasicDetailForm(forms.ModelForm):
    random_number = forms.CharField(widget=forms.HiddenInput(), required=False)
    terms_accepted = forms.BooleanField(required=True, error_messages={'required': 'You must accept the terms and conditions to proceed.'})

    class Meta:
        model = crebasicdetailform
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
        recent_applications = crebasicdetailform.objects.filter(
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
       

