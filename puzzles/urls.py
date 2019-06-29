from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('search/', views.index, name='puzzle_index'),
    path('update/', views.update, name='puzzle_update'),
    path('search/<slug:search>', views.detail, name='puzzle_detail'),
]
