# under by Andy import
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo, name='todo'),
    path('create/', views.createtodo, name='createtodo'),
    path('view/<int:id>', views.viewtodo, name='viewtodo'),
    path('completed/', views.completed, name='completed'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('completed/<int:id>', views.completed_by_id, name='completed_by_id'),
    path('sort/', views.sorttodo, name='sort'),
    path('fitness/', views.fitness, name='fitness'),
    path('bmi/', views.bmi, name='bmi'),
    path('sogi/', views.sogi, name='sogi'),
    path('pwindex/', views.pwindex, name='pwindex'),
    path('genpassword/', views.genpassword, name='genpassword'),
]
