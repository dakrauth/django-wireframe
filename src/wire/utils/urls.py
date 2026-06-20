from functools import cache

from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


@cache
def full_domain():
    scheme = settings.URL_SCHEME
    domain = get_current_site(None).domain
    if domain.endswith("/"):
        domain = domain[:-1]

    return f"{scheme}{domain}"


def full_reverse(*args, **kwargs):
    local_path = reverse(*args, **kwargs)
    return f"{full_domain()}{local_path}"
