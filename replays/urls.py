from django.urls import include, path
from django.contrib import admin

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:replay_id>', views.detail, name='detail'),
    path('reproduce/<int:replay_id>', views.reprod, name='reprod'),
]
