from django.urls import path
from . import views

urlpatterns=[
    path('customer_review/', views.customer_review),
]