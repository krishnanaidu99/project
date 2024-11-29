from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import *
from .forms import *

def personal_detail_view(request, instance_id=None):
    if instance_id:
        personal_details = get_object_or_404(PersonalDetail, id=instance_id)
    else:
        personal_details = None
    
    if request.method == 'POST':
        form = PersonalDetailForm(request.POST, request.FILES, instance=personal_details)
        if form.is_valid():
            personal_details = form.save()
            return redirect('document_detail', instance_id=personal_details.id)
    else:
        form = PersonalDetailForm(instance=personal_details)
    
    random_number = personal_details.random_number if personal_details else None
    return render(request, 'main/personal_detail_form.html', {'form': form, 'random_number': random_number})


def document_detail_view(request, instance_id):
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    document_upload, created = DocumentUpload.objects.get_or_create(personal_detail=personal_detail)
  
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=document_upload)
        if form.is_valid():
            form.save()
            return redirect('success')  
    else:
        form = DocumentUploadForm(instance=document_upload)

    return render(request, 'admin/document_upload_form.html', {'form': form,'random_number':personal_detail.random_number if personal_detail and personal_detail.random_number else None})

# ====================homelaon======================

def customer_profile_view(request, instance_id=None):
    customer_profile = get_object_or_404(CustomerProfile, id=instance_id) if instance_id else None
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            customer_profile = form.save()
            print(f"Redirecting to 'applicant_document_create' with id: {customer_profile.id}")  # Debug print
            return redirect('applicant_document_create', instance_id=customer_profile.id)
        else:
            print(f"Form errors: {form.errors}")  
    else:
        form = CustomerProfileForm(instance=customer_profile)

    return render(request, 'main/customer_profile_form.html', {'form': form, 'random_number': customer_profile.random_number if customer_profile and customer_profile.random_number else None})

def applicant_document_create_view(request, instance_id):
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    
    # Use filter() to handle multiple documents
    applicant_documents = ApplicantDocument.objects.filter(applicant_profile=applicant_profile)
    
    if applicant_documents.exists():
        applicant_document = applicant_documents.first()  # or any other logic to choose a document
    else:
        applicant_document = ApplicantDocument(applicant_profile=applicant_profile)

    if request.method == 'POST':
        form = ApplicantDocumentForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form = ApplicantDocumentForm(instance=applicant_document)
    
    return render(request, 'admin/applicant_document_form.html', {
        'form': form,
        'random_number': applicant_profile.random_number if applicant_profile and applicant_profile.random_number else None,
        'incomesource': applicant_profile.income_source,
        'loan_type': applicant_profile.loan_type,
    })
def plbasicdetails(request):
    form = plBasicDetailForm()

    if request.method == 'POST':
        form = plBasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('personal') 
        
    return render(request, 'admin/plbasicdetail.html',{'form':form})

def hlbasicdetails(request):
    form = hlBasicDetailForm()

    if request.method == 'POST':
        form = hlBasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('customer_profile') 
        
    return render(request, 'main/hlbasicdetail.html',{'form':form})


def success(request):
    return render(request, 'admin/success.html')



#views and updates==================================================

def update_personal_detail_view(request, pk):
    personal_detail = get_object_or_404(PersonalDetail, pk=pk)
    if request.method == 'POST':
        form = PersonalDetailForm(request.POST, instance=personal_detail)
        if form.is_valid():
            form.save()
            return redirect('update_document_detail', instance_id=personal_detail.id)
    else:
        form = PersonalDetailForm(instance=personal_detail)
    return render(request, 'main/personal_detail_form.html', {'form': form})

def update_document_detail_view(request, instance_id):
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    document_upload, created = DocumentUpload.objects.get_or_create(personal_detail=personal_detail)
  
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=document_upload)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DocumentUploadForm(instance=document_upload)

    return render(request, 'admin/document_upload_form.html', {'form': form})

def personal_detail_list_view(request):
    personal_details = PersonalDetail.objects.all()
    return render(request, 'admin/personal_detail_list.html', {'personal_details': personal_details})
def document_upload_list_view(request):
    document_uploads = DocumentUpload.objects.select_related('personal_detail').all()
    return render(request, 'admin/document_upload_list.html', {'document_uploads': document_uploads})
def view_personal_detail_view(request, pk):
    personal_detail = get_object_or_404(PersonalDetail, pk=pk)
    return render(request, 'admin/view_personal_detail.html', {'personal_detail': personal_detail})
def view_documents_view(request, pk):
    document_upload = get_object_or_404(DocumentUpload, pk=pk)
    return render(request, 'admin/view_documents.html', {'document_upload': document_upload})


def update_customer_profile_view(request, pk):
    customer_profile = get_object_or_404(CustomerProfile, pk=pk)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            return redirect('applicant_document_create', instance_id=customer_profile.id )
    else:
        form = CustomerProfileForm(instance=customer_profile)

    return render(request, 'main/customer_profile_form.html', {'form': form})


def update_applicant_document_view(request, instance_id):
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    applicant_document, created = ApplicantDocument.objects.get_or_create(applicant_profile=applicant_profile)

    if request.method == 'POST':
        form = ApplicantDocumentForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = ApplicantDocumentForm(instance=applicant_document)

    return render(request, 'admin/applicant_document_form.html', {'form': form})
def customer_profile_list_view(request):
    customer_profiles = CustomerProfile.objects.all()
    return render(request, 'admin/customer_profile_list.html', {'customer_profiles': customer_profiles})

def applicant_document_list_view(request):
    applicant_documents = ApplicantDocument.objects.select_related('applicant_profile').all()
    return render(request, 'admin/applicant_document_list.html', {'applicant_documents': applicant_documents})

def view_customer_profile_view(request, pk):
    customer_profile = get_object_or_404(CustomerProfile, pk=pk)
    return render(request, 'admin/view_customer_profile.html', {'customer_profile': customer_profile})


def view_applicant_document_view(request, pk):
    applicant_document = get_object_or_404(ApplicantDocument, pk=pk)
    return render(request, 'admin/view_applicant.html', {'applicant_document': applicant_document})




def personal_detail_list_view(request):
    personal_details = PersonalDetail.objects.all()
    return render(request, 'admin/personal_detail_list.html', {'personal_details': personal_details})

def customer_profile_list_view(request):
    customer_profiles = CustomerProfile.objects.all()
    return render(request, 'admin/customer_profile_list.html', {'customer_profiles': customer_profiles})
def dashboard(request):
    return render(request, 'main/admin.html')
 

def personal_verification_add(request, instance_id):
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    
    # Use filter() to handle multiple documents
    applicant_documents = ApplicationVerification.objects.filter(personal_detail=personal_detail)
    
    if applicant_documents.exists():
        applicant_document = applicant_documents.first()  # or any other logic to choose a document
    else:
        applicant_document = ApplicationVerification(personal_detail=personal_detail)

    if request.method == 'POST':
        form = ApplicationVerificationForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form = ApplicationVerificationForm(instance=applicant_document)
    
    return render(request, 'admin/applyper.html', {
        'form': form,})

def update_personal_verify(request, instance_id):
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    # Retrieve or create the document upload instance associated with the personal_details
    applicant_document, created = ApplicationVerification.objects.get_or_create(personal_detail=personal_detail)

    if request.method == 'POST':
        form = ApplicationVerificationForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            # Redirect to a success page or back to the update page
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form =ApplicationVerificationForm(instance=applicant_document)

    return render(request, 'admin/update_per.html', {
        'form': form,
        
    })

def personalcustomerverify(request, instance_id):
    # Fetch the loan application based on the given instance_id
    personal_detail = get_object_or_404(PersonalDetail, id=instance_id)
    
    # Fetch existing verification documents for this loan application
    verfyObj = ApplicationVerification.objects.filter(personal_detail=personal_detail).first()
    
    # Check if the session email matches the loan application email
    session_email = request.session.get('email')
    random_number = None
    if session_email and session_email == personal_detail.email:
        random_number = personal_detail.random_number
    
    # Render the record details in the template
    return render(request, 'admin/perview.html', {
        'personal_detail': personal_detail,
        'verfyObj': verfyObj,
        'random_number': random_number,  # Pass the random_number to the template
    })


def home_verification_add(request, instance_id):
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    
    # Use filter() to handle multiple documents
    applicant_documents = HomeApplication.objects.filter(applicant_profile=applicant_profile)
    
    if applicant_documents.exists():
        applicant_document = applicant_documents.first()  # or any other logic to choose a document
    else:
        applicant_document = HomeApplication(applicant_profile=applicant_profile)

    if request.method == 'POST':
        form = HomeapplicationForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form = ApplicationVerificationForm(instance=applicant_document)
    
    return render(request, 'admin/applyhome.html', {'form': form,})


def update_home_verify(request, instance_id):
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    # Retrieve or create the document upload instance associated with the personal_details
    applicant_document, created = HomeApplication.objects.get_or_create(applicant_profile=applicant_profile)

    if request.method == 'POST':
        form = HomeapplicationForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            # Redirect to a success page or back to the update page
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form =HomeapplicationForm(instance=applicant_document)

    return render(request, 'admin/update_home.html', {
        'form': form,
        
    })

def homecustomerverify(request, instance_id):
    # Fetch the loan application based on the given instance_id
    applicant_profile = get_object_or_404(CustomerProfile, id=instance_id)
    
    # Fetch existing verification documents for this loan application
    verfyObj = HomeApplication.objects.filter(applicant_profile=applicant_profile).first()
    
    # Check if the session email matches the loan application email
    session_email = request.session.get('email')
    random_number = None
    if session_email and session_email == applicant_profile.email_id:
        random_number = applicant_profile.random_number
    
    # Render the record details in the template
    return render(request, 'admin/homeview.html', {
        'applicant_profile': applicant_profile,
        'verfyObj': verfyObj,
        'random_number': random_number,  # Pass the random_number to the template
    })