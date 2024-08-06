from django.apps import AppConfig
import os 
from django.conf import settings



class TestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testapp'

    def ready(self):
        # Ensure MEDIA_ROOT exists
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
