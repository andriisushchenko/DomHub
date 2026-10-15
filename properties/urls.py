from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/create/', views.property_create, name='property_create'),
    path('property/<int:pk>/edit/', views.property_update, name='property_update'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('register/', views.register, name='register'),
]
