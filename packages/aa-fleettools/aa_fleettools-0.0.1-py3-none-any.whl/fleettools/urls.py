from django.urls import path

from . import views

app_name = 'fleettools'

urlpatterns = [
    path('', views.index, name='index'),
    path('fleetmover/', views.fleetmoverlogin, name='fleetmoverlogin'),
    path('fleetmover/<int:token_pk>/', views.fleetmover, name='fleetmover'),
]
