from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
import logging
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.http import HttpResponse
from django.contrib import auth

from ravi.models import *
from business.models import *
from bhanu.models import Educationalloan

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def Login(request):
    if request.method == 'POST':#IF THE CONDITION IS TRUE IT SHOULD ENTER INTO THE IF CONDITION
       username = request.POST['username'] 
       password = request.POST['password']  

       user = auth.authenticate(username=username,password=password)
       if user is not None:
           auth.login(request, user)
           print('login is successfully')
           return redirect('dashboard')
       else:
           print('invalid credentials')
           return redirect('login')
    else:
        return render(request,'customer/login.html')

def lap_add(request, instance_id=None):
    customer_profile = get_object_or_404(LoanApplication, id=instance_id) if instance_id else None
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, request.FILES, instance=customer_profile)
        if form.is_valid():
            customer_profile = form.save()
            print(f"Redirecting to 'applicant_document_create' with id: {customer_profile.id}")  # Debug print
            return redirect('lapdoc', instance_id=customer_profile.id)
        else:
            print(f"Form errors: {form.errors}")  
    else:
        form = LoanApplicationForm(instance=customer_profile)

    return render(request, 'customer/LAPform.html', {'form': form, 'random_number': customer_profile.random_number if customer_profile and customer_profile.random_number else None})

def lap_document_add(request, instance_id):
    personal_details = get_object_or_404(LoanApplication, id=instance_id)
    
    # Use filter() to handle multiple documents
    applicant_documents = lapDocumentUpload.objects.filter(personal_details=personal_details)
    
    if applicant_documents.exists():
        applicant_document = applicant_documents.first()  # or any other logic to choose a document
    else:
        applicant_document = lapDocumentUpload(personal_details=personal_details)

    if request.method == 'POST':
        form = LapDocumentUploadForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form = LapDocumentUploadForm(instance=applicant_document)
    
    return render(request, 'customer/lapdoc.html', {
        'form': form,
        'random_number': personal_details.random_number if personal_details and personal_details.random_number else None,
        'incomesource': personal_details.income_source,
        'loan_type': personal_details.loan_type,
    })
def goldbasicdetails(request):
    form = goldBasicDetailForm()

    if request.method == 'POST':
        form = goldBasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('goldloan_application')
        print(f"form error is:{form.errors}") 
       
    return render(request, 'customer/goldbasicdetail.html',{'form':form})

def basicdetails(request):
    form = BasicDetailForm()

    if request.method == 'POST':
        form = BasicDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('lapapply')
        print(f"form error is:{form.errors}")
        
    return render(request, 'customer/basicdetailform.html',{'form':form})


            # Check the loan type and redirect accordingly
    #         if instance.loantype == 'personalloan':
    #             return redirect('personal')  # Change 'personal_page' to your actual URL name
    #         elif instance.loantype == 'homeloan':
    #             return redirect('customer_profile')  # Change 'home_loan_page' to your actual URL name
    #         elif instance.loantype == 'educationloan':
    #             return redirect('education_add')
    #         elif instance.loantype == 'lap':
    #             return redirect('lapapply') 
    #         elif instance.loantype == 'goldloan':
    #             return redirect('goldloan_application') 
    #         elif instance.loantype == 'creditcard':
    #             return redirect('credit_add') 
    #         elif instance.loantype == 'businessloan':
    #             return redirect('demo') 
    #         elif instance.loantype == 'carloan':
    #             return redirect('car_loan_application')   
    #         else:
    #             return redirect('basicdetail')  # Change 'default_page' to your actual URL name

    # else:
    #     form = BasicDetailForm(instance=instance)

    # context = {
    #     'form': form,
    #     'random_number': instance.random_number if instance and instance.random_number else None,
    # }

    


def success(request):
    return render(request, 'customer/success.html')



#views and updates==================================================




def update_lap(request, pk):
    customer_profile = get_object_or_404(LoanApplication, pk=pk)
    if request.method == 'POST':
        form = LoanApplicationForm(request.POST, instance=customer_profile)
        if form.is_valid():
            form.save()
            # Redirect to update_lapdoc with the instance_id of the updated loan application
            return redirect('update_doc', instance_id=customer_profile.id)
    else:
        form = LoanApplicationForm(instance=customer_profile)

    return render(request, 'customer/LAPform.html', {'form': form,})

def update_lapdoc(request, instance_id):
    personal_details = get_object_or_404(LoanApplication, id=instance_id)
    # Retrieve or create the document upload instance associated with the personal_details
    applicant_document, created = lapDocumentUpload.objects.get_or_create(personal_details=personal_details)

    if request.method == 'POST':
        form = LapDocumentUploadForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
        
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form = LapDocumentUploadForm(instance=applicant_document)

    return render(request, 'customer/lapdoc.html', {
        'form': form,
        
        'incomesource': personal_details.income_source,
        'loan_type': personal_details.loan_type,
    })
def lapview(request):
    customer_profiles = LoanApplication.objects.all()
    return render(request, 'customer/lap_view.html', {'customer_profiles': customer_profiles})

def lapdocview(request):
    applicant_documents = lapDocumentUpload.objects.select_related('personal_details').all()
    return render(request, 'customer/docview.html', {'applicant_documents': applicant_documents})

def lapbuttview(request, pk):
    customer_profile = get_object_or_404(LoanApplication, pk=pk)
    return render(request, 'customer/lap_viewbutton.html', {'customer_profile': customer_profile})


def lapdocbutt(request, pk):
    applicant_document = get_object_or_404(lapDocumentUpload, pk=pk)
    return render(request, 'customer/view_docbutt.html', {'applicant_document': applicant_document})



def goldloanapplication(request, instance_id=None):
    if instance_id:
        instance = get_object_or_404(Goldloanapplication, id=instance_id)  # Correctly reference the model
    else:
        instance = None

    if request.method == 'POST':
        form = goldform(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save()
            return redirect('goldloan_application', instance_id=instance.id)  # Redirect to the same view with the instance_id
    else:
        form = goldform(instance=instance)

    context = {
        'form': form,
        'random_number': instance.random_number if instance and instance.random_number else None,
    }

    return render(request, 'customer/goldloan.html', context)

def goldview(request):
    customer_profiles = Goldloanapplication.objects.all()
    return render(request, 'customer/viewgoldloan.html', {'customer_profiles': customer_profiles})

# def goldbuttview(request, pk):
#     applicant_document = get_object_or_404(Goldloanapplication, pk=pk)
#     return render(request, 'customer/view_lapdoc.html', {'applicant_document': applicant_document})
from django.conf import settings


def generate_otp():
    """Generate a 6-digit OTP."""
    return ''.join(random.choices(string.digits, k=6))

def send_otp(email, otp_code):
    """Send OTP code to the provided email."""
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def generate_verify_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        
        if otp:
            # Verify OTP
            try:
                otp_entry = OTP.objects.get(otp=otp, expires_at__gte=timezone.now())
                request.session['email'] = otp_entry.email
                return redirect('index')
            except OTP.DoesNotExist:
                return render(request, 'customer/generate_verify_otp.html', {
                    'form': OTPForm(), 
                    'error': 'Invalid or expired OTP',
                    'email': email
                })
        
        # Generate OTP
        if email:
            otp_code = generate_otp()
            OTP.objects.create(email=email, otp=otp_code, expires_at=timezone.now() + timezone.timedelta(minutes=5))
            send_otp(email, otp_code)
            return render(request, 'customer/generate_verify_otp.html', {
                'form': OTPForm(),
                'email': email
            })
    
    return render(request, 'customer/generate_verify_otp.html', {
        'form': OTPForm()
    })
def index(request):
    # Fetch the email from the session
    email = request.session.get('email')
    
    # Filter loan applications based on the session email
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    
    # Render the index page with the filtered list of loans and email
    return render(request, 'index.html', {
        'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,
        'email': email,
    })



def lap_verification_add(request, instance_id):
    # Retrieve the loan application
    loan = get_object_or_404(LoanApplication, id=instance_id)
    
    # Retrieve or create the document
    applicant_documents = lapApplicationVerification.objects.filter(loan=loan)
    if applicant_documents.exists():
        applicant_document = applicant_documents.first()  # Get the first document if exists
    else:
        applicant_document = lapApplicationVerification(loan=loan)
    
    # Handle form submission
    if request.method == 'POST':
        form = lapApplicationVerifyForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to a success page or another view
        else:
            print('Form errors:', form.errors)
    else:
        form = lapApplicationVerifyForm(instance=applicant_document)
    
    return render(request, 'customer/lapappliverify.html', {
        'form': form,
          # Pass a flag to indicate update or add
    })
def update_lapverify(request, instance_id):
    loan = get_object_or_404(LoanApplication, id=instance_id)
    # Retrieve or create the document upload instance associated with the personal_details
    applicant_document, created = lapApplicationVerification.objects.get_or_create(loan=loan)

    if request.method == 'POST':
        form = lapApplicationVerifyForm(request.POST, request.FILES, instance=applicant_document)
        if form.is_valid():
            form.save()
            # Redirect to a success page or back to the update page
            return redirect('success')
        else:
            print('Form errors:', form.errors)
    else:
        form = lapApplicationVerifyForm(instance=applicant_document)

    return render(request, 'customer/updateverify.html', {
        'form': form,
        
    })

def lapcustomerverify(request, instance_id):
    # Fetch the loan application based on the given instance_id
    loan = get_object_or_404(LoanApplication, id=instance_id)
    
    # Fetch existing verification documents for this loan application
    verfyObj = lapApplicationVerification.objects.filter(loan=loan).first()
    
    # Check if the session email matches the loan application email
    session_email = request.session.get('email')
    random_number = None
    if session_email and session_email == loan.email_id:
        random_number = loan.random_number
    
    # Render the record details in the template
    return render(request, 'customer/customerverify.html', {
        'loan': loan,
        'verfyObj': verfyObj,
        'random_number': random_number,  # Pass the random_number to the template
    })


def custom_logout(request):
    logout(request)
    return redirect('send_otp') 





def LoanAgainstProperty(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'LoanAgainstProperty.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})



from django.shortcuts import render

# Create your views here.

def About(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'About.html', {'email': email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})



def Allinsurance(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    
    # Render the index page with the filtered list of loans and email
    
    form=InsuranceForm()
    if request.method=='POST':
        form=InsuranceForm(request.POST)
        form.save()
        return HttpResponse("data saved")
    
    return render(request,'AllInsurance.html',{'form':form,'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl,})
def allinsurance_view(request):
    all=AllInsurance.objects.all()
    return render(request,'customer/view_insurance.html',{'all':all})
def lifeinsurance_view(request):
    life=LifeInsurance.objects.all()
    return render(request,'customer/view_lifeinsurance.html',{'life':life})

def generalinsurance_view(request):
    general=GeneralInsurance.objects.all()
    return render(request,'customer/view_generalinsurance.html',{'general':general})
    

def healthinsurance_view(request):
    health=healthInsurance.objects.all()
    return render(request,'customer/view_healthinsurance.html',{'health':health})
    

    

def Generalinsurance(request):
    
    
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    
    form=genInsuranceForm()
    if request.method=='POST':
        form=genInsuranceForm(request.POST)
        form.save()
        return HttpResponse("data saved")

    return render(request, 'GeneralInsurance.html',{'form':form,'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})



def Healthinsurance(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    email = request.session.get('email')
    form=healthInsuranceForm()
    if request.method=='POST':
        form=healthInsuranceForm(request.POST)
        form.save()
        return HttpResponse("data saved")
    else:
       return render(request, 'HealthInsurance.html',{'form':'form','email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def Lifeinsurance(request):
    
    email = request.session.get('email')
    
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    form=lifeInsuranceForm()
    if request.method=='POST':
        form=lifeInsuranceForm(request.POST)
        form.save()
        return HttpResponse("data saved")
    else:
       
       return render(request, 'LifeInsurance.html',{'form':form,'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})
    

def BussinessLoan(request):

    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'BussinessLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def CarLoan(request):
    
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'CarLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def contact(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'contact.html',{'email': email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def creditpage(request):
  
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'creditpage.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def dsa(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'dsa.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def educationalloan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'Educationalloan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def franchise(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'franchise.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})



def GoldLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'GoldLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})


def HomeLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'HomeLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def LoanAgainstProperty(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'LoanAgainstProperty.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def NewCarLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'NewCarLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def Personalloans(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'Personalloans.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})

def UsedCarLoan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'UsedCarLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})


def homeloan(request):
    email = request.session.get('email')
    loans = LoanApplication.objects.filter(email_id=email)
    edu = Educationalloan.objects.filter(mail_id=email)
    bus=BusinessLoan.objects.filter(email_id=email)
    pl = PersonalDetail.objects.filter(email=email)
    hl=CustomerProfile.objects.filter(email_id=email)
    return render(request, 'HomeLoan.html',{'email':email,'loans': loans,'edu':edu,'bus':bus,'pl':pl,'hl':hl})
# =======================bhanu=====================================







