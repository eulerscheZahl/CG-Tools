from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='puzzle_index'),
    path('stats/', views.stats, name='puzzle_stats'),
    path('update/', views.update, name='puzzle_update'),
]
