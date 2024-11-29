from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('personal/', views.personal_detail_view, name='personal'),
    path('personal/<int:instance_id>/', views.personal_detail_view, name='personal_detail'),
    path('personaldoc/<int:instance_id>/', views.document_detail_view, name='document_detail'),
    path('home/', views.customer_profile_view, name='customer_profile'),
    path('home/<int:instance_id>/', views.customer_profile_view, name='customer_profile_detail'),
    path('homedoc/<int:instance_id>/', views.applicant_document_create_view, name='applicant_document_create'),
    path('plbasicdetail/', views.plbasicdetails, name='plbasicdetail'),
    path('hlbasicdetail/', views.hlbasicdetails, name='hlbasicdetail'),
    path('success/', views.success, name='success'),
    path('personal/<int:pk>/update/', views.update_personal_detail_view, name='update_personal_detail'),
    path('personal/<int:pk>/view/', views.view_personal_detail_view, name='view_personal_detail'),
    path('personal/details/', views.personal_detail_list_view, name='personal_detail_list'),
    path('document/<int:instance_id>/update/', views.update_document_detail_view, name='update_document_detail'),
    path('document/uploads/', views.document_upload_list_view, name='document_upload_list'),
    path('document/upload/<int:pk>/view/', views.view_documents_view, name='view_documents'),
    path('home/<int:pk>/update/', views.update_customer_profile_view, name='update_customer_profile'),
    path('home/<int:pk>/view/', views.view_customer_profile_view, name='view_customer_profile'),  
    path('home/profiles/', views.customer_profile_list_view, name='customer_profile_list'),
    path('applicant/<int:instance_id>/update/', views.update_applicant_document_view, name='update_applicant_document'),
    path('applicant/documents/', views.applicant_document_list_view, name='applicant_document_list'),
    path('applicant/<int:pk>/view/', views.view_applicant_document_view, name='view_applicant_document'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perstatus/<int:instance_id>/', views.personal_verification_add, name='personal_verification_add'),
    path('perstatus/<int:instance_id>/update/', views.update_personal_verify, name='update_personal_verify'),
    path('perstatus/<int:instance_id>/view', views.personalcustomerverify, name='view_personal_verify'),
    path('applyhome/<int:instance_id>/', views.home_verification_add, name='applyhome'),
    path('applyhome/<int:instance_id>/update/', views.update_home_verify, name='update_home_verify'),
    path('applyhome/<int:instance_id>/view', views.homecustomerverify, name='view_home_verify'),
    
]