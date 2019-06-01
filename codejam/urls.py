from django.urls import include, path, re_path
from django.contrib import admin

from . import views

urlpatterns = [
    path('search/', views.index, name='index'),
    re_path(r'^search/(?P<search>[\w\d\-_\.@]+)$', views.detail, name='detail'),
    #path('update/', views.update, name='update'),
    #path('update2/', views.update2, name='update2'),
    path('ajax/autocomplete/', views.autocomplete, name='ajax_autocomplete')
]
