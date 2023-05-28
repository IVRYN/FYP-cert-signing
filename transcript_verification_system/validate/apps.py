from django.apps import AppConfig


class ValidateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'validate'

    def ready(self):
        from . import signals
