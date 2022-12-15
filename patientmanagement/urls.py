from django.urls import path

from . import views
# from views import *


urlpatterns = [
    path('', views.plha_listing, name='plha_listing'),
    path('plha_test', views.plha_test, name='plha_test'),
    path('index', views.index, name='index'),
    path('patient_register', views.patient_register, name='patient_register'),
    path('add_registration', views.add_registration, name='add_registration'),
    path('PatientRegistration', views.PatientRegistration, name='PatientRegistration'),

]