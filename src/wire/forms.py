from django import forms
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm

from wire.mail import send_labeled_mail


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
