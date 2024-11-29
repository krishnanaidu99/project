from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import *
# Create your views here.


def demo(request):
    return HttpResponse("hi Your Project Working Fine")


def apply_for_business_loan(request):
    if request.method == 'POST':
        form = BusinessLoanForm(request.POST)
        if form.is_valid():
            businessObj=form.save()
            request.session['business_id']=businessObj.id
            return redirect('upload-documents')
        else:
            print(form.errors)
            return render(request,'apply_for_business_loan.html',{'form': form})
       
    else:
        form = BusinessLoanForm()
    
    return render(request, 'apply_for_business_loan.html', {'form': form})


def upload_documents(request):
    if request.method == 'POST':
        if request.session.get('business_id'):
            loanid = request.session.get('business_id')
            print(loanid)
            loanObj = get_object_or_404(BusinessLoan, id=loanid)

            form = BusinessLoanDocumentForm(request.POST, request.FILES)

            if form.is_valid():
                docObj = form.save(commit=False)
                docObj.loan = loanObj
                docObj.save()
                return HttpResponse('Created Document with Application Id of - {}'.format(loanObj.application_id))
            else:
                # If the form is not valid, re-render the form with errors
                print(form.errors)
                return render(request, 'Bussiness_upload_documents.html', {'form': form})
    else:
        form = BusinessLoanDocumentForm()
    
    return render(request, 'BussinessUploadDocuments.html', {'form': form})


# def insuranceForm(request):
#     if request.method=='POST':
#         form=InsuranceForm(request.POST)
#         form.save()
#         return HttpResponse("data saved")
#     else:
#         return render(request,'Insurance.html')


def business_loan_list(request):
    business_loans = BusinessLoan.objects.all()
    return render(request, 'business_loan_list.html', {'business_loans': business_loans})

def business_loan_update(request,application_id):
    loan = get_object_or_404(BusinessLoan, application_id=application_id)
    print(loan.id)
    if request.method == 'POST':
        form = BusinessLoanForm(request.POST, instance=loan,instance_id=loan.id)
        if form.is_valid():
            form.save()
            return HttpResponse('Updated')
        else:
            print(form.errors)
            return render(request, 'business_loan_update.html', {'form': form})

    else:
        form = BusinessLoanForm(instance=loan)
    return render(request, 'business_loan_update.html', {'form': form})

def business_loan_view(request,id):
    if BusinessLoan.objects.filter(id=id).exists():
        businessObj=BusinessLoan.objects.get(id=id)
        form=BusinessLoanForm(instance=businessObj)
        return render(request,'business_loan_view.html',{'form':form})
    

def documentsView(request,application_id,loan=None):
    try:
      loan = get_object_or_404(BusinessLoan.objects.prefetch_related('BussinessLoandocuments'),application_id=application_id)
      document = loan.BussinessLoandocuments 
    
    except Exception as e:
     return HttpResponse("No Documents Found...")


    if request.method=='GET':
         
         form = BusinessLoanDocumentForm(instance=document)
    
    return render(request, 'ViewBusDocument.html', {'form': form, 'loan': loan})




def update_business_loan_document(request,application_id,loan=None):
    
    try:
      loan = get_object_or_404(BusinessLoan.objects.prefetch_related('BussinessLoandocuments'),application_id=application_id)
      document = loan.BussinessLoandocuments 
    
    except Exception as e:
     return HttpResponse("No Documents Found...")
    
    if request.method == 'POST':
        form = BusinessLoanDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
        #    docObj = form.save(commit=False)
        #    docObj.loan = loan
        #    docObj.save()
           form.save()
           return HttpResponse('Document Updated')
        else:
            print(form.errors)
            return render(request, 'UpdateBusinessLoanDocument.html', {'form': form, 'loan': loan})

    else:
         print('hiiii')
         print(document.aadhar_card_front)
         form = BusinessLoanDocumentForm(instance=document)
    
    return render(request, 'UpdateBusinessLoanDocument.html', {'form': form, 'loan': loan})



def applicationVerification(request,application_id,loan=None):

    loan=BusinessLoan.objects.get(application_id=application_id)
    if request.method == 'POST':
        form = ApplicationVerifyForm(request.POST)
        if form.is_valid():
          try:
            verifiObj=form.save(commit=False)
            verifiObj.loan=loan
            verifiObj.save()
            return HttpResponse("success")
          except:
              return HttpResponse("Verification already applied...")
        else:
            print(form.errors)
            return HttpResponse("Invalid form data", status=400)  # Return a response for invalid form data
    else:
        form = ApplicationVerifyForm()
        return render(request, 'ApplicationVerification.html', {'form': form})
    

def update_verification(request,application_id,loan=None):

    try:
        loan=get_object_or_404(BusinessLoan.objects.prefetch_related('applicationverification'),application_id=application_id)
        verifObj=loan.applicationverification

    except Exception as e:
        return HttpResponse("No Verification details found...")
    
    if request.method=='GET':
        form=ApplicationVerifyForm(instance=verifObj)
        return render(request,"UpdateVerification.html",{'form':form})
    else:
         form = ApplicationVerifyForm(request.POST,instance=verifObj)
         if form.is_valid():
           docObj = form.save(commit=False)
           docObj.loan = loan
           docObj.save()
           return HttpResponse('Updated Verification..')
         else:
            print(form.errors)
            return render(request,"UpdateVerification.html",{'form':form})
        


         
         
def customerProfile(request,application_id,loan=None):
     try:
      loan=get_object_or_404(BusinessLoan.objects.prefetch_related('applicationverification'),application_id=application_id)
      try:
       verfyObj=loan.applicationverification
      except:
          verfyObj=None
         
     except Exception as e:
         verfyObj=None
         return HttpResponse("No records Found..")
     
     if request.method=='GET':
      if request.session.get('email') and request.session.get('email')==loan.email_id:
        del request.session['email']
        return render(request,"CustomerProfile.html",{'loan':loan,'verfyObj':verfyObj})


def busbasicdetails(request):
    form = busBasicDetailForm()

    if request.method == 'POST':
        form = busBasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('add_bussiness') 
        
    return render(request, 'busbasicdetail.html',{'form':form})

     
     
         
     

    
    


    