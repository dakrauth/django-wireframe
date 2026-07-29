from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.tokens import default_token_generator

from wire.models import WireLog
from wire.forms import PasswordResetForm, PasswordInitializeForm


@admin.register(WireLog)
class WireLogAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "sub_label", "created")
    list_filter = ("label",)
    ordering = ("-created",)


class UserAdmin(auth_admin.UserAdmin):
    actions = ["send_password_reset", "send_password_initializion"]
    password_reset_form_class = PasswordResetForm
    password_init_form_class = PasswordInitializeForm

    def send_password_email(self, request, queryset, form_class):
        for user in queryset:
            if not user.email:
                self.message_user(request, f"User {user} skipped: no email")
                continue

            form = form_class(user, {"email": user.email})
            form.full_clean()
            form.save(use_https=request.is_secure(), request=request)

    def send_password_initializion(self, request, queryset):
        self.send_password_email(request, queryset, self.password_init_form_class)
    send_password_initializion.short_description = "Send password initialization email to selected users"

    @admin.action(description="Send Password Reset Email")
    def send_password_reset(self, request, queryset):
        self.send_password_email(request, queryset, self.password_reset_form_class)
    send_password_reset.short_description = "Send password reset email to selected users"
