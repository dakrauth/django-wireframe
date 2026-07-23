from django import forms
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm

from wire.mail import send_labeled_mail


DEFAULT_MONOSPACED_TEXTAREA_ATTRS = {"cols": "72", "rows": "15"}


class PasswordResetForm(BasePasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        send_labeled_mail(
            "password_reset",
            context=context,
            recipients=[to_email],
        )


class MonospacedTextarea(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = getattr(
            settings,
            "WIRE_MONOSPACED_TEXTAREA_ATTRS",
            DEFAULT_MONOSPACED_TEXTAREA_ATTRS
        )
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
