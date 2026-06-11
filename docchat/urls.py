from django.urls import path
from . import views

urlpatterns=[
    path('docchat/', views.doc_chat),
]