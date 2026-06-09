from django.urls import path
from . import views

urlpatterns=[
    path('email_subject/', views.email_subject_generator),
]