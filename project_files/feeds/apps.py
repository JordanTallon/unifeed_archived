from django.apps import AppConfig


class FeedsSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feeds'

    def ready(self):
        from . import signals
