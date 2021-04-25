import sys
from django.apps import AppConfig


class OnlineComputerStoreConfig(AppConfig):
    name = 'onlineComputerStore'
    verbose_name = "Online Computer Store"

    def ready(self):
        # initialized the application
        if 'runserver' not in sys.argv:
            return True





