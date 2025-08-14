from django.apps import AppConfig
from django.db.models.signals import post_save


class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'relationship_app'

    def ready(self):
        from django.contrib.auth import get_user_model
        from .signals import create_user_profile
        post_save.connect(create_user_profile, sender=get_user_model())
