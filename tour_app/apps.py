from django.apps import AppConfig


class TourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tour_app'

    def ready(self):
        import tour_app.signals