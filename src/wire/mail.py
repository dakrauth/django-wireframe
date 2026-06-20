#!/usr/bin/env python
import itertools
from datetime import datetime

import requests

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail.backends.base import BaseEmailBackend
from django.template import loader, TemplateDoesNotExist

from wire.models import wirelog
from wire.logger import getLogger

logger = getLogger(__name__)
counter = itertools.count(1)


class MailgunEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        results = []
        for e in email_messages:
            html_message = None
            alt = e.alternatives
            if alt and alt[0][1] == "text/html":
                html_message = alt[0][0]

            status = send_mail(
                e.subject,
                e.body,
                recipient_list=e.to,
                html_message=html_message,
                from_email=e.from_email,
                cc=e.cc,
                bcc=e.bcc,
            )
            results.append(status)
        return results


def debug_mail(**params):
    info = []
    temp_mail_dir = settings.BASE_DIR / "temp/mail"
    temp_mail_dir.mkdir(parents=True, exist_ok=True)
    file_base = temp_mail_dir / f"{next(counter)}-{datetime.now().isoformat()}"
    for key, value in params.items():
        if key in ["html", "text"]:
            fn = file_base.with_suffix(f".{key}")
            fn.write_text(value)
            value = fn

        info.append(f"... {key.capitalize()}: {value}")

    logger.warning("Sending email\n{}".format("\n".join(info)))


def send_mail(
    subject,
    message,
    recipient_list=None,
    html_message=None,
    from_email=None,
    cc=None,
    bcc=None,
    **extras,
):
    data = {
        "from": from_email or settings.MAILGUN["from_email"],
        "subject": subject,
        "text": message or "",
    }

    if html_message:
        data["html"] = html_message

    if cc:
        data["cc"] = cc

    if bcc:
        data["bcc"] = bcc
        if not recipient_list:
            recipient_list = from_email

    recipient_list = recipient_list or settings.MAILGUN["admin_email"]
    if isinstance(recipient_list, str):
        recipient_list = [recipient_list]

    data["to"] = recipient_list
    if settings.DEBUG:
        if settings.MAILGUN.get("send_debug", False):
            data["to"] = ["dakrauth@gmail.com"]
        else:
            debug_mail(**data)
            return 1

    try:
        r = requests.post(
            settings.MAILGUN["url"], auth=("api", settings.MAILGUN["api_key"]), data=data
        )
    except Exception as exc:
        logger.exception("Mailgun failure")
        result = "FAIL"
        msg = str(exc)
    else:
        result = r.status_code
        try:
            msg = r.json()
        except requests.JSONDecodeError:
            msg = r.content.decode()

    if getattr(settings, "WIRELOG_EMAILS", False):
        wirelog(
            "mailgun",
            sub_label=data["subject"],
            status=str(result),
            data={
                "to": data["to"],
                "from": data["from"],
                "subject": data["subject"],
                "result": result,
                "details": msg,
            },
        )

    return result


def pretty_email(recipient):
    if isinstance(recipient, (list, tuple)):
        name, email = recipient
        return f'"{name}" <{email}>'

    return recipient


class LabeledEmailer:
    template_base_dir = getattr(settings, "WIRE_LABELS_BASE", "wire/labels")

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs.pop(key))

        self.kwargs = kwargs

    def render_label(self, label, format, context, using=None):
        """
        Returns a rendered string with the given label and formt
        """
        try:
            return loader.render_to_string(
                f"{self.template_base_dir}/{label}/{format}", context=context, using=using
            )
        except TemplateDoesNotExist:
            return ""

    def format_label(self, label, context, subject=None):
        if not subject:
            subject = self.render_label(label, "subject.txt", context, using="text")

        subject = " ".join(subject.split())
        if not subject:
            raise ValueError(f"Missing email subject for label {label}")

        text = self.render_label(label, "body.txt", context, using="text").lstrip()
        html = self.render_label(label, "body.html", context)
        return subject, text, html

    def send(
        self,
        label,
        context=None,
        recipients=None,
        subject=None,
        cc=None,
        bcc=None,
        from_email=None,
    ):
        context = context or {}
        context.update(
            site=Site.objects.get_current(),
            url_scheme=settings.URL_SCHEME,
        )

        if not isinstance(recipients, (list, tuple)):
            recipients = [recipients]

        subject, message, html = self.format_label(label, context, subject)
        recipient_list = [pretty_email(recip) for recip in recipients]
        if cc:
            cc = [pretty_email(recip) for recip in cc]

        if bcc:
            bcc = [pretty_email(recip) for recip in bcc]

        return send_mail(
            subject,
            message,
            recipient_list,
            html_message=html,
            from_email=from_email,
            cc=cc,
            bcc=bcc,
        )


def __send_mail_sdk(
    subject,
    message=None,
    recipient_list=None,
    html_message=None,
    from_email=None,
    cc=None,
):
    from mailgun.client import Client

    domain = settings.MAILGUN["url"]
    recipient_list = recipient_list or settings.MAILGUN["admin_email"]
    if isinstance(recipient_list, str):
        recipient_list = [recipient_list]

    data = {
        "from": from_email or settings.MAILGUN["from_email"],
        "to": recipient_list,
        "subject": subject,
        "text": message or "",
        # "o:tag": "Python test",
    }

    if html_message:
        data["html"] = html_message

    with Client(auth=("api", settings.MAILGUN["api_key"])) as client:
        req = client.messages.create(data=data, domain=domain)

    print(req.json())


labeled_emailer = LabeledEmailer()
