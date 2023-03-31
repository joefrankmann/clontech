from ndx_result_source.templatetags.result import *  # noqa
import ndx_result_source.templatetags.result as source  # noqa

import json
from django import template
from django.utils.html import escape
register = template.Library()


@register.simple_tag
def go_stix_value(gostix, interpretation):
    if interpretation == 'OffScale':
        return 'Off Scale'
    return gostix


@register.simple_tag
def teststrip_graph_data(teststrip):
    return escape(json.dumps({
        'profile': teststrip.profile,
        'baseline': teststrip.baseline,
        'c_peak_position': teststrip.cline_peak_position,
        't_peak_position': teststrip.tlines.first().peak_position,
    }))
