from django.core.management.base import BaseCommand

from ndx_result.models import Result


class Command(BaseCommand):
    help = "generate CSV rows for results which do not have them"

    def handle(self, *args, **kwargs):
        for result in Result.objects.all():
            if not result.generated_csv_row:
                result.save_csv_row()
