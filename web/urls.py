from django.urls import path
from .views import account
# by lanfc


urlpatterns = [
    path('send/sms', account.send_sms, name='send_sms'),
    path('register', account.register, name='register'),
    path('smsreg', account.smsregister, name='smsreg'),

    #path('redis', views.getredis),
]