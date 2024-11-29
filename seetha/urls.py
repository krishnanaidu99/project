"""
URL configuration for ddproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from seetha.views import *

from django.conf.urls.static import static
from django.conf import  settings

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('car-loan-application/',apply_for_car_loan,name='car-loan-application'),
    path('document/',car_upload_documents,name="car-upload-documents"),
    path('car-loans-list/',car_loan_list, name='car_loan_list'),
    path('car-loan-update/<str:application_id>',car_loan_update,name='car-loan-update'),
    path('car-loan-view/<str:id>',car_loan_view,name='car-loan-view'),
    path('document-upload/<str:application_id>',update_car_loan_document,name='update-documents'),
    path('car-view-document/<str:application_id>',documentsView,name='car-documents-view'),
    path('carbasicdetail/',carbasicdetails,name="carbasicdetail"),

]







urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
