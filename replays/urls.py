from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('analyze/', views.analyze, name='analyze'),
    path('reproduce/', views.reprod, name='reprod'),
]
