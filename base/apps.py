from django.apps import AppConfig


class BaseConfig(AppConfig):
    #The implicit primary key type to add to models within this app. You can use this to keep AutoField as the primary key type for third party applications.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'