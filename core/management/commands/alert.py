from django.core.management.base import BaseCommand

from core.datatools.alert import Alert


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            alert = Alert()
            alert.run()
        except KeyboardInterrupt:
            pass
