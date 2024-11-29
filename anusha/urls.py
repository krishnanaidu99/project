
from django.urls import path
from anusha import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView



urlpatterns = [

    path('basicdetail/',views.basicdetails,name='basicdetail'),
path('goldbasicdetail/',views.goldbasicdetails,name='goldbasicdetail'),
    path('viewinsurance/',views.allinsurance_view,name='insuranceview'),
    path('viewlifeinsurance/',views.lifeinsurance_view,name='insurancelifeview'),
     path('viewgeninsurance/',views.generalinsurance_view,name='insurancegenview'),
    path('viewhealthinsurance/',views.healthinsurance_view,name='insurancehealthview'),


    path('login/',views.Login,name='login'),
    # path('basicdetail/<int:instance_id>/',views.basicdetail,name='basicdetail'),
         path('generate-verify-otp/', views.generate_verify_otp_view, name='generate-verify-otp'),

# ===============================================
    path('lapapply/', views.lap_add, name='lapapply'),
    # path('lapapply/<int:instance_id>/', views.lap_add, name='lapapply_add'),
    path('lapapply/<int:instance_id>/', views.lap_document_add, name='lapdoc'),
    path('lapverify/<int:instance_id>/', views.lap_verification_add, name='lapverify'),
    path('lapverify/<int:instance_id>/update/', views.update_lapverify, name='update_verify'),
    path('lapverify/<int:instance_id>/view', views.lapcustomerverify, name='viewcustomerverify'),  
  

    path('lapapply/<int:pk>/update/', views.update_lap, name='update_lap'),
    path('lapapply/profiles/', views.lapview, name='lapview'),
    path('lapapply/<int:pk>/view/', views.lapbuttview, name='viewbutt'),  

    path('doclap/<int:instance_id>/update/', views.update_lapdoc, name='update_doc'),
    path('doclap/documents/', views.lapdocview, name='docview'),
    path('doclap/<int:pk>/view/', views.lapdocbutt, name='viewdocbutt'),

    # =============================================================================
    path('goldloan/', views.goldloanapplication, name='goldloan_application'),
    path('goldloan/<int:instance_id>/', views.goldloanapplication, name='goldloan_application'),
    path('goldloan/profiles/', views.goldview, name='goldview'),
    # path('goldloan/<int:pk>/view/', views.goldbuttview, name='goldviewbutt'), 
    
    
    #=============================================
   
    path('success/', views.success, name='success'),
#     ===========================================================
    path('',views.index,name='index'),
    path('about/',views.About,name='about'),
    path('allinsurance/',views.Allinsurance,name='allinsurance'),
    
    path('bussinessLoan/',views.BussinessLoan,name='bussinessloan'),
    path('carloan/',views.CarLoan,name='carloan'),
    path('contact/',views.contact,name='contact'),
    path('creditpage/',views.creditpage,name='creditpage'),
    path('dsa/',views.dsa,name='dsa'),
    path('educationalloan/',views.educationalloan,name='educationalloan'),
    path('franchise/',views.franchise,name='franchise'),
    path('generalinsurance/',views.Generalinsurance,name='generalinsurance'),
    path('gold/',views.GoldLoan,name='gold'),
    path('healthinsurance/',views.Healthinsurance,name='healthinsurance'),
    path('lifeinsurance/',views.Lifeinsurance,name='lifeinsurance'),
    path('loanagainstproperty/',views.LoanAgainstProperty,name='lap'),
    path('newcarloan/',views.NewCarLoan,name='newcar'),
    path('personalloans/',views.Personalloans,name='personalloans'),
    path('usedcarloan/',views.UsedCarLoan,name='usedcar'),
    path('homeloan/',views.HomeLoan,name='homeloan'),
    # ==============bhanu==================================================
    
    
    
    



]