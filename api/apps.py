from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # This method is called when the app is ready.
        # We import and call our model loader here.
        from . import services
        services.summarize_text("Pre-loading summarizer...")
