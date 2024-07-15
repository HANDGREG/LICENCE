from django.urls import path
from .views import *



urlpatterns = [
    path('', home, name='home'),
    path('candidat/', candidat_list, name='candidat_list'),
    path('candidat/detail/<str:id>/', candidat_detail, name='candidat_detail'),
    path('candidat/vote/<str:id>/', vote, name='vote'),
    path('login/',connexion, name='login'),
   
]