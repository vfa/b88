from django.urls import path
from . import views
# by lanfc

app_name = 'app01'

urlpatterns = [
    path('send/sms', views.send_sms),
    path('register', views.register),
    path('redis', views.getredis),
]