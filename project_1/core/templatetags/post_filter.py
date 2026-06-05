import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def hashtags_to_links(text):
    return mark_safe(
        re.sub(
            r"#(\w+)",
            r'<a href="/tag/\1/">#\1</a>',
            text
        )
    )