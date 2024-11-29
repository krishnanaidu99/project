from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .forms import *
from .forms import CarLoanForm
from .forms import CarLoanDocumentForm

def demo(request):
    return HttpResponse("hi Your Project Working Fine")

def carbasicdetails(request):
    form = carBasicDetailForm()

    if request.method == 'POST':
        form = carBasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            return redirect('car-loan-application') 
        
    return render(request, 'carbasicdetail.html',{'form':form})

def apply_for_car_loan(request):
    print("View function called")
    if request.method == 'POST':
        form = CarLoanForm(request.POST)
        if form.is_valid():
            # print("Form is valid")
            carObj=form.save()
            form.save()
            # return redirect("success")
            request.session['car_id']=carObj.application_id
            return redirect('car-upload-documents')
        else:
            print(form.errors)
            print("errors")
            return render(request,'apply_for_car_loan.html',{'form': form})
       
    else:
        form = CarLoanForm()
    
    return render(request, 'apply_for_car_loan.html', {'form': form})
    


def car_loan_list(request):
    car_loans = CarLoan.objects.all()
    return render(request, 'car_loan_list.html', {'car_loans': car_loans})

def car_loan_update(request,application_id):
    loan = get_object_or_404(CarLoan, application_id=application_id)
    print(loan)
    if request.method == 'POST':
        form = CarLoanForm(request.POST, instance=loan,instance_id=loan.id)
        if form.is_valid():
            form.save()
            return HttpResponse('Updated')
        else:
            print(form.errors)
            return render(request, 'car_loan_update.html', {'form': form})

    else:
        form = CarLoanForm(instance=loan)
    return render(request, 'car_loan_update.html', {'form': form})


def car_loan_view(request,id):
    if CarLoan.objects.filter(id=id).exists():
        carObj=CarLoan.objects.get(id=id)
        form=CarLoanForm(instance=carObj)
        return render(request,'car_loan_view.html',{'form':form})

def car_upload_documents(request):
    car_loan_id = request.session.get('car_id')  # Get car loan ID from session
    if not car_loan_id:
        return redirect('apply_for_car_loan')  # Redirect if car loan ID is not in session

    car_loan = get_object_or_404(CarLoan, application_id=car_loan_id)  # Fetch the car loan application
    
    if request.method == 'POST':
        print('post')
        form = CarLoanDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            documents = form.save(commit=False)
            documents.loan = car_loan  # Link the documents to the car loan application
            documents.save()
            return HttpResponse('Created Document with Application Id of - {}'.format(car_loan.application_id))
            # return HttpResponse("sucess..")
            # return redirect('sucess')  # Redirect to a success page after upload
        else: 
            print("Form is invalid")
            print(form.errors)
            return render(request, 'Car_upload_documents.html', {'form': form, 'loan': car_loan})
    else:
        
        form = CarLoanDocumentForm()

    return render(request, 'Car_upload_documents.html', {'form': form, 'loan': car_loan})


def documentsView(request,application_id,loan=None):
    try:
      loan = get_object_or_404(CarLoan.objects.prefetch_related('CarLoandocuments'),application_id=application_id)
      document = loan.CarLoandocuments 
    
    except Exception as e:
     return HttpResponse("No Documents Found...")

    if request.method=='GET':
         
        form = CarLoanDocumentForm(instance=document)
    
    return render(request, 'ViewDocument.html', {'form': form, 'loan': loan})


def update_car_loan_document(request,application_id,loan=None):
    
    try:
      loan = get_object_or_404(CarLoan.objects.prefetch_related('CarLoandocuments'),application_id=application_id)
      document = loan.CarLoandocuments 
    
    except Exception as e:
     return HttpResponse("No Documents Found...")
    
    if request.method == 'POST':
        form = CarLoanDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
           docObj = form.save(commit=False)
           docObj.loan = loan
           docObj.save()
           return HttpResponse('Document Updated')
        else:
            print(form.errors)

    else:
         print('hiiii')
         form = CarLoanDocumentForm(instance=document)
    
    return render(request, 'update_car_loan_document.html', {'form': form, 'loan': loan})
