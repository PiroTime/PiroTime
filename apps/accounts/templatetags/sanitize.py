from django import template
from django.utils.safestring import mark_safe

from apps.accounts.sanitize import clean_html

register = template.Library()


@register.filter
def sanitize(value):
    """`|safe` 대신 사용: 허용된 서식 태그만 남기고 출력한다."""
    return mark_safe(clean_html(value))
