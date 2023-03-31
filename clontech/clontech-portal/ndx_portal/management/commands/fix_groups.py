from django.core.management.base import BaseCommand
from ndx_portal.fix_group_names import fix_group_names


class Command(BaseCommand):
    help = 'Fix group names. Only after the data transfer script.'

    def handle(self, *args, **options):
        fix_group_names()
