from django.contrib import admin
from django.urls import path
from pay import views 
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from .views import MobileRecharge2



urlpatterns = [
    path('', views.homeView.as_view(), name='home'),
    path('registration/',  views.registration.as_view(), name='registration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'pay/login.html', authentication_form = LoginForm) , name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('AddAccount/', views.AddAccountView.as_view(), name = "AddAccount"),
    path('AccountPass/', views.AccountPassView.as_view(), name='AccountPass'),
    path('Success/', views.Success, name='Success'),
    path('AccountDetail/', views.AccountDetail.as_view(), name='AccountDetail'),
    path('Balance/', views.BalanceView.as_view(), name='Balance'),
    path('NextProcess/', views.NextProcess.as_view(), name='NextProcess'),
    path('NextProcess/TransectionSuccess/', views.TransectionSuccess, name='TransectionSuccess'),
    path('TransectionHistory/', views.TransectionHistory.as_view(), name='TransectionHistory'),
    path('MobileRecharge/', views.MobileRecharge, name='MobileRecharge'),
    path('MobileRecharge2/', views.MobileRecharge2.as_view(), name='MobileRecharge2'),
    path('MobileRechargeSuccess/', views.MobileRechargeSuccess, name='MobileRechargeSuccess'),
   
   

    
]