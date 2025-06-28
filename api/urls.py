
from django.urls import path, include
from api import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('PaybuddyAPI/', views.PaybuddyAPI.as_view(), name='PaybuddyAPI'),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('gettoken/', obtain_auth_token),
    path('paymentdone/', views.paymentdone.as_view(), name='paymentdone'),
    path('paymentcancel/',views.paymentcancel, name='paymentcancel'),
   
]


