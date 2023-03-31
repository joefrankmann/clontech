from typing import Sequence

from django.conf import settings
from django.db.models import signals
from django.dispatch import receiver

from .models import Batch
from .tasks import create_missing_data_matrices


@receiver(signals.post_save, sender=Batch, dispatch_uid='ndx_batch_save')
def batch_post_save(
        raw: bool = None,
        update_fields: Sequence[str] = (),
        **kwargs) -> None:
    if raw:
        return None
    if update_fields and 'lot_no' not in update_fields:
        return None
    if settings.NDX_CREATE_MISSING_DATA_MATRICES_ON_SAVE:
        create_missing_data_matrices.delay()
