from django.db import transaction
import celery

from . import data_matrix


@celery.shared_task(autoretry_for=(Exception,))
def create_missing_data_matrices() -> None:
    with transaction.atomic():
        data_matrix.create_missing_data_matrices()
