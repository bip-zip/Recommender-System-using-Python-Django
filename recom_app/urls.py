from django.conf.urls import url
from .views import *
from django.urls import path,include


app_name='recom_app'

urlpatterns=[
    path("index/", IndexView.as_view(), name="home")

]