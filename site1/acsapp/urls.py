from django.contrib import admin
from django.urls import path, include
from acsapp import views

urlpatterns = [
    path('download/<docid>/', views.download, name='download'),
]
