from django.core.files.base import ContentFile
import pystrich
import pystrich.datamatrix

from .models import Batch


def create_data_matrix_for_batch(batch: Batch) -> bytes:
    """Returns a datamatrix of the batches lot_no as a PNG image."""
    return pystrich.datamatrix.DataMatrixEncoder(batch.lot_no).get_imagedata()


def create_missing_data_matrices() -> None:
    """Creates all data matrices that are missing."""
    for batch in Batch.objects.filter(data_matrix='').select_for_update():
        matrix_data = ContentFile(create_data_matrix_for_batch(batch))
        batch.data_matrix.save('{}.png'.format(batch.lot_no), matrix_data)
        batch.save()
