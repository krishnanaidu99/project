from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *

def crebasicdetails(request):
    form = creBasicDetailForm()

    if request.method == 'POST':
        form = creBasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('creditappli_add') 
        
    return render(request, 'crebasicdetail.html',{'form':form})

# # Create your views here.

# def credit_card_add(request):
#     form=CreditCardApplicationForm()
#     if request.method=='POST':
#           form=CreditCardApplicationForm (request.POST,request.FILES)
#           if form.is_valid():
#                cred=form.save()
#                return redirect('creditdoc_add',instance_id=cred.id)
#           print(f"Form errors: {form.errors}")
#     return render(request,'credit_add.html',{'form':form})

def credit_card_add(request, instance_id=None):
    customer_profile = get_object_or_404(CreditCardApplication, id=instance_id) if instance_id else None
    if request.method == 'POST':
        form = CreditCardApplicationForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            customer_profile = form.save()
            print(f"Redirecting to 'applicant_document_create' with id: {customer_profile.id}") 
            return redirect('creditdoc_add', instance_id=customer_profile.id)
        else:
            print(f"Form errors: {form.errors}")  
    else:
        form = CreditCardApplicationForm(instance=customer_profile)

    return render(request, 'credit_add.html', {'form': form, 'random_number': customer_profile.random_number if customer_profile and customer_profile.random_number else None})




def update(request, pk):
    personal_detail = get_object_or_404(CreditCardApplication, pk=pk)
    if request.method == 'POST':
        form = CreditCardApplicationForm(request.POST, instance=personal_detail)
        if form.is_valid():
            form.save()
            return redirect('creditdoc_add', instance_id=personal_detail.id)  # Ensure this matches your URL pattern
    else:
        form = CreditCardApplicationForm(instance=personal_detail)

    return render(request, 'creditappli_update.html', {'form': form})


def creditappli_show(request, pk):
    personal_detail= get_object_or_404(CreditCardApplication, pk=pk)
    return render(request, 'creditappli_show.html', {'personal_detail':personal_detail })




# ////////////////////////////documents///////////////////////////////////////////


def upload_documents(request,instance_id):
    personal_details=get_object_or_404(CreditCardApplication,id=instance_id)
    applicant,created=CreditDocumentUpload.objects.get_or_create(personal_details=personal_details)
    if request.method=='POST':
          form=DocumentUploadForm(request.POST,request.FILES,instance=applicant)
          if form.is_valid():
               form.save()
               return redirect('ok')
          print(f"Form errors: {form.errors}")
    else:
        form=DocumentUploadForm(instance=applicant)
    return render(request,'creditdoc_add.html',{'form':form,'random_number': personal_details.random_number})




def success(request):
    return render(request,'ok.html')




def view(request):
     data=CreditCardApplication.objects.all()
     return render(request,'creditappli_view.html',{'data':data})



# def creditdoc_show(request, pk):
#     document = get_object_or_404(CreditDocumentUpload, pk=pk)
#     return render(request, 'document_show.html', {'document': document})



# def creditdoc_show(request, instance_id):
#     personal_details = get_object_or_404(CreditCardApplication, id=instance_id)
#     applicant = get_object_or_404(CreditDocumentUpload, personal_details=personal_details)
    
#     documents = applicant.documents.all()  # Get all documents associated with this applicant
    
#     return render(request, 'creditdoc_show.html', {'documents': documents, 'instance_id': instance_id})




# def creditdoc_show(request, instance_id):
#     personal_details= get_object_or_404(CreditDocumentUpload, id=instance_id)
#     return render(request, 'creditdoc_show.html',{'personal_details':personal_details })




# def creditdoc_show(request, instance_id):
#     personal_details = get_object_or_404(CreditCardApplication, id=instance_id)
#     applicant = CreditDocumentUpload.objects.filter(personal_details=personal_details)
#     return render(request, 'creditdoc_show.html', {'applicant': applicant})


def creditdoc_show(request):
    applicant_documents = CreditDocumentUpload.objects.select_related('personal_details').all()
    return render(request, 'creditdoc_show.html', {'applicant_documents': applicant_documents})

def creditdoc_button(request, pk):
    applicant_document = get_object_or_404(CreditDocumentUpload, pk=pk)
    return render(request, 'creditdocbutton.html', {'applicant_document': applicant_document})












def docupdate(request, instance_id):
    personal_detail = get_object_or_404(CreditDocumentUpload, id=instance_id)
    document_upload, created = CreditDocumentUpload.objects.get_or_create(personal_detail=personal_detail)
  
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=document_upload)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DocumentUploadForm(instance=document_upload)

    return render(request, 'document_update.html',{'form':form})











