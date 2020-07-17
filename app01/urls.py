from django.urls import path
from . import views
# by lanfc


urlpatterns = [
    path('', views.send_sms),
]