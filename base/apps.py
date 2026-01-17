from django.apps import AppConfig

class BaseConfig(AppConfig):
    # Configuration class for the 'base' app
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField as the default primary key field
    name = 'base'  # Name of the app, used in settings.py and other configurations
