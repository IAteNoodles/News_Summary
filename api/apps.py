from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # This method is called when the app is ready.
        # We import and call our model loader here.
        # --- DISABLED PRE-LOADING ---
        # The Phi-4 model is too large to pre-load on most consumer GPUs.
        # It will now be lazy-loaded on the first API request instead.
        # from . import services
        # services.summarize_text("Pre-loading summarizer...")
        pass
