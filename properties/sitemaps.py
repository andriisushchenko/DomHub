from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Property


class StaticSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['home', 'property_list']

    def location(self, item):
        return reverse(item)


class PropertySitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return Property.objects.filter(is_active=True).order_by('-created_at')

    def lastmod(self, obj):
        return obj.updated_at
