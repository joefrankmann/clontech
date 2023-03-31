from django.core.management.base import BaseCommand

from ndx_result.models import Result


class Command(BaseCommand):
    help = "regenerate all CSV rows"

    def handle(self, *args, **kwargs):
        for result in Result.objects.all():
            result.save_csv_row()
