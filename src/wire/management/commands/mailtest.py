import sys

from django.conf import settings
from django.core.mail import send_mail
from django.test import RequestFactory
from django.core.management.base import BaseCommand

from wire.utils.debug import technical_500_response


class Command(BaseCommand):
    help = "Send a test email through mailgun"

    def handle(self, *args, **options):
        request = RequestFactory().get("/oops/")
        try:
            raise RuntimeError("You asked for it!")
        except Exception:
            exc_info = sys.exc_info()

        text, html = technical_500_response(request, *exc_info)
        recipient_list = [settings.ADMINS[0][1]]
        r = send_mail(
            "Test subject for Mailgun",
            text,
            from_email=None,
            recipient_list=recipient_list,
            html_message=html,
        )
        print(f"Response was {r}")
