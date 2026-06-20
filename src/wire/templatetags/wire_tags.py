from django import template
from django.utils.safestring import mark_safe

from wire.markdown import markdown as mkdn

register = template.Library()


class BlockNotOverriddenError(NotImplementedError):
    pass


@register.simple_tag
def ensure_overridden():
    raise BlockNotOverriddenError


@register.filter
def markdown(text):
    return mark_safe(mkdn(text))
