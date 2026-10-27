from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    name = 'properties'

    def ready(self):
        from . import signals
