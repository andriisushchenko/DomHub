from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Agent, Category, Property, PropertyImage


@receiver([post_save, post_delete])
def clear_api_cache(sender, **kwargs):
    if sender in (Property, PropertyImage, Category, Agent):
        cache.clear()
