from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [

    path('',views.home, name='home'),
    path('date/',views.date_extract, name='output')
    
]
