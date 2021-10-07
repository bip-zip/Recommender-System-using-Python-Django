from django.conf.urls import url
from .views import *
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView  

app_name='accounts'

urlpatterns=[
    path("", LoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
]