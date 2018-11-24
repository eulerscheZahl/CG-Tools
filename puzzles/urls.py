from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('search/', views.index, name='index'),
    path('update/', views.update, name='update'),
    path('search/<slug:search>', views.detail, name='detail'),
]
