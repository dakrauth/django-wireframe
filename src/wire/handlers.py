from django.utils.log import AdminEmailHandler


# Unfortunately, this belongs here to avoid django.core.exceptions.AppRegistryNotReady errors
class WireEmailHandler(AdminEmailHandler):
    def send_mail(self, subject, message, *args, **kwargs):
        from .mail import send_mail

        send_mail(
            subject,
            message,
            html_message=kwargs.get("html_message", None),
            from_email=None,
        )
