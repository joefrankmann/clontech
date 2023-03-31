from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def eula_classes(context, eula):
    classes = [eula.status]
    if eula.is_valid_from_in_future:
        classes.append('future')
    if eula == context.get('current_eula'):
        classes.append('current')
        classes.append('info')
    if not eula.is_active:
        classes.append('text-muted')
    return ' '.join(classes)
