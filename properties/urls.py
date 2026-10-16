from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views, views

router = DefaultRouter()
router.register('properties', api_views.PropertyViewSet)
router.register('categories', api_views.CategoryViewSet)
router.register('agents', api_views.AgentViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/create/', views.property_create, name='property_create'),
    path('property/<int:pk>/edit/', views.property_update, name='property_update'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('register/', views.register, name='register'),
    path('api/', include(router.urls)),
]
