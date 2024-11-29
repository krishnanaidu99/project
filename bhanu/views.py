from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from .forms import *
from django.http import HttpResponse

# Create your views here.

def edubasicdetails(request):
    form = eduBasicDetailForm()

    if request.method == 'POST':
        form = eduBasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('createEducationloan') 
        
    return render(request, 'ebasicdetail.html',{'form':form})



def create_EducationLoan(request):
    if request.method == 'POST':
        form = EducationalLoanForm(request.POST, request.FILES)
        if form.is_valid():
            loan=form.save()
            request.session['loanid']=loan.id
            return redirect('create-doc')
       
    else:
        form = EducationalLoanForm()
    
    return render(request, 'Apply_EducationLoan.html', {'form': form})


def loan_records(request):
    records = Educationalloan.objects.all()
    return render(request, 'loan_records.html', {'records': records})


def update_record(request, id):
    record = Educationalloan.objects.get(id=id)
    if request.method == 'POST':
        form = EducationalLoanForm(request.POST,request.FILES,instance=record,instance_id=id)
        if form.is_valid():
            form.save()
            return HttpResponse("Updated")
        else:
            print(form.errors)
    else:
        form = EducationalLoanForm(instance=record)
    return render(request, 'EducationLoanUpdate.html', {'form': form})


def viewEducationLoan(request,id):
    record = Educationalloan.objects.get(id=id)
    form = EducationalLoanForm(instance=record)
    return render(request, 'EducationLoanView.html', {'form': form})



def createDocuments(request):
    
    if request.method=='GET':
       
        form= DocumentsForm()
        return render(request,'CreateDocuments.html',{'form':form})
    else:
       if request.session.get('loanid'):
            loanid = request.session.get('loanid')
            print(loanid)
            loanObj = get_object_or_404(Educationalloan, id=loanid)

            form = DocumentsForm(request.POST, request.FILES)

            if form.is_valid():
                docObj = form.save(commit=False)
                docObj.loan = loanObj
                docObj.save()
                return HttpResponse('Created Document')
            else:
                # If the form is not valid, re-render the form with errors
                return render(request, 'CreateDocuments.html', {'form': form})
       else:
            # Handle the case where loanid is not in the session
            return HttpResponse('No loan ID exist')
           
      
       
def document_list(request):
      documents = Educationloan_document_upload.objects.all()
      return render(request, 'document_list.html', {'documents': documents})




def updateDocument(request,application_id,loan=None):
    try:
      loan = get_object_or_404(Educationalloan.objects.prefetch_related('personal_details'), application_id=application_id)
      document = loan.personal_details

    except:
        return HttpResponse("No Documents Found...")
    if request.method=='GET':
     form=DocumentsForm(instance=document)
     return render(request,'DocumentUpdate.html',{'form':form})
    
    form = DocumentsForm(request.POST, request.FILES, instance=document)
    if form.is_valid():
        #    docObj = form.save(commit=False)
        #    docObj.loan = loan
        #    docObj.save()
           form.save()
           return HttpResponse('Document Updated')
    else:
        print(form.errors)
        return render(request,'DocumentUpdate.html',{'form':form})
    


def viewDocuments(request,application_id,loan=None):
    try:
      loan = get_object_or_404(Educationalloan.objects.prefetch_related('personal_details'), application_id=application_id)
      document = loan.personal_details
    except:
        return HttpResponse("No Documents Found...")
    
    form=DocumentsForm(instance=document)
    return render(request,'ViewDocument.html',{'form':form})
    


def applicationVerification(request,application_id,loan=None):

    try:
     print("first")
     loan=Educationalloan.objects.get(application_id=application_id)
    except:
        return HttpResponse("No Records Found..")
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
        loan=get_object_or_404(Educationalloan.objects.prefetch_related('applicationverification'),application_id=application_id)
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
      loan=get_object_or_404(Educationalloan.objects.prefetch_related('applicationverification'),application_id=application_id)
      try:
       verfyObj=loan.applicationverification
      except:
          verfyObj=None
         
     except Exception as e:
         verfyObj=None
         return HttpResponse("No records Found..")
     
     if request.method=='GET':
         email=request.session.get('email')
         if email and email==loan.mail_id:
          del request.session['email']
          return render(request,"CustomerProfile.html",{'loan':loan,'verfyObj':verfyObj})
         else:
             return HttpResponse("Please login..Login Page")


