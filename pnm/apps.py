from django.apps import AppConfig


class PnmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pnm'

    def ready(self):
        import pnm.signals