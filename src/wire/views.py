from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.decorators import user_passes_test

from wire.forms import PasswordResetForm


def group_required(*group_names):
    def in_groups(user):
        if user.is_authenticated and user.is_active:
            return user.is_superuser or user.groups.filter(name__in=group_names).exists()

    return user_passes_test(in_groups)


class StaffRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
