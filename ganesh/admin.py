from django.contrib import admin
from .models import *

@admin.register(CreditCardApplication)
class CreditCardApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email_address', 'phone_number', 'employment_status', 
        'monthly_annual_income', 'total_monthly_expenses', 'terms_and_conditions_agreed', 
        'privacy_policy_agreed', 'electronic_signature')
    
    




# '///////////////////////////////////////////////'


admin.site.register(CreditDocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('id','get_proof_of_identity_filename',
                    'get_proof_of_address_filename',
                    'get_proof_of_income_filename',)