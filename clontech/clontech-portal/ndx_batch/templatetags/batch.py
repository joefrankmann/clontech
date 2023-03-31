from django import template

from ..models import Batch

register = template.Library()


@register.simple_tag()
def batch_classes(batch: Batch):
    classes = [batch.status]
    if batch.is_valid_from_in_future:
        classes.append('future')
    return ' '.join(classes)
