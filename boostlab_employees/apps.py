from django.apps import AppConfig


class BoostlabEmployeesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boostlab_employees'


    def ready(self):
        import boostlab_employees.signals