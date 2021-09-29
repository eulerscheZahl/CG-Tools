from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='leaderboards_index'),
    path('update/', views.update, name='leaderboards_update'),
]
