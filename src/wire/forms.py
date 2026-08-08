from django import forms
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm

from wire.mail import send_labeled_mail


DEFAULT_MONOSPACED_TEXTAREA_ATTRS = {"cols": "72", "rows": "15"}


class BasePasswordForm(BasePasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        link = reverse(
            "password_reset_confirm",
            kwargs={"uidb64": kwargs["uid"], "token": kwargs["token"]}
        )

        kwargs.update(
            title=self.title,
            preheader=self.preheader,
            salutation=f"Hello,",
            lines=[
                self.description_line.format(**kwargs),
                "Please click on the link below and choose a new password.",
            ],
            url_scheme=kwargs["protocol"],
            link=link,
            link_text=self.link_text,
        )
        return kwargs

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
            context=self.get_context_data(**context),
            recipients=[to_email],
        )

class PasswordResetForm(BasePasswordForm):
    title = "Password Reset"
    preheader = "Password Reset"
    description_line = "You're receiving this email because you requested a password reset for your user account at {site_name}."
    link_text = "Reset Password"


class PasswordInitializeForm(BasePasswordForm):
    title = "Password Initialization"
    preheader = "Password Initialization"
    description_line = "You're receiving this email because you need to set a password for your user account at {site_name}."
    link_text = "Initialize Password"


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
