"""
URL configuration for khammam project.

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
from ganesh import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
    path('creditappli_add/',views.credit_card_add,name='creditappli_add'),
        path('creditappli_add/<int:instance_id>',views.credit_card_add,name='creditappli_add'),

    path('creditdoc_add/<int:instance_id>',views.upload_documents,name='creditdoc_add'),
    path('success/',views.success,name='ok'),
    path('creditappli_view/',views.view,name='creditappli_view'),
    path('update/<int:pk>',views.update,name='update'),
    path('update/<int:pk>',views.docupdate,name='docupdate'),
    path('crebasicdetail/',views.crebasicdetails,name='crebasicdetail'),



    path('creditappli_view/<int:pk>/views/',views. creditappli_show,name='creditappli_show'),
    path('document_view/', views.creditdoc_show, name='creditdoc_show'),
    path('document_view/<int:pk>', views.creditdoc_button, name='creditdoc_button'),





]

if settings.DEBUG:
 urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
