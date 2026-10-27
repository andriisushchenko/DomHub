from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views, views
from .sitemaps import PropertySitemap, StaticSitemap

router = DefaultRouter()
router.register('properties', api_views.PropertyViewSet)
router.register('categories', api_views.CategoryViewSet)
router.register('agents', api_views.AgentViewSet)

sitemaps = {
    'static': StaticSitemap,
    'properties': PropertySitemap,
}

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', views.property_list, name='property_list'),
    path('map/', views.property_map, name='property_map'),
    path('map/data/', views.property_map_data, name='property_map_data'),
    path('stats/', views.property_stats, name='property_stats'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/create/', views.property_create, name='property_create'),
    path('property/<int:pk>/edit/', views.property_update, name='property_update'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('register/', views.register, name='register'),
    path('api/', include(router.urls)),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]
