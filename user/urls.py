"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include


from .import views

urlpatterns = [
    path('', views.userhome),
    path('viewproducts/', views.viewproducts),
    path('subcatviewproducts/', views.subcatviewproducts),
    path('addproducts/', views.addproducts),
    path('showSubCategory/', views.showSubCategory),
    path('editprofileuser/', views.editprofileuser),
    path('updateDataUser/',views.updateDataUser),
    path('changepassworduser/',views.changepassworduser),
    path('viewproductuser/',views.viewproductuser),
    path('payment/',views.payment),
    path('cancel/',views.cancel),
    path('viewbiddingproducts/',views.viewbiddingproducts),
    path('bidproduct/',views.bidproduct),
    path('mybid/',views.mybid),
    path('viewbid/',views.viewbid)

]
