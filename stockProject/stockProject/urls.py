"""stockProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from stockApp import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #DASHBOARD
    path('', login_required(views.Dashboard.as_view(), login_url='login')),
    
    #LOGIN & LOGOUT
    path('login', views.AdminLogin.as_view(), name='login'),
    path('logout', views.AdminLogout.as_view()),
    
    #PRODUCTS
    path('products', login_required(views.Products.as_view(), login_url='login')),
    path('product-edit/<int:pk>', login_required(views.ProductUpdate.as_view(), login_url='login'), name='editProd'),
    path('product-remove/<int:pk>', login_required(views.ProductRemove.as_view(), login_url='login'), name='removeProd'),
    
    #BRANDS
    path('brands', login_required(views.Brands.as_view(), login_url='login')),
    path('brand-edit/<int:pk>', login_required(views.BrandUpdate.as_view(), login_url='login'), name='editBrand'),
    path('brand-remove/<int:pk>', login_required(views.BrandRemove.as_view(), login_url='login'), name='removeBrand'),
    
    #USERS
    path('users', login_required(views.UserListView.as_view(), login_url='login')),
    path('user-edit/<int:pk>', login_required(views.UserUpdate.as_view(), login_url='login'), name='editUser'),
    path('user-remove/<int:pk>', login_required(views.UserRemove.as_view(), login_url='login'), name='removeUser'),

    #STORES
    path('stores', login_required(views.StoreListView.as_view(), login_url='login')),
    path('store-edit/<int:pk>', login_required(views.StoreUpdate.as_view(), login_url='login'), name='editStore'),
    path('store-remove/<int:pk>', login_required(views.StoreRemove.as_view(), login_url='login'), name='removeStore'),
    
    #CHARTS
    path('barchart', login_required(views.Barchart.as_view(), login_url='login')),    

]