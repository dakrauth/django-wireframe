from django.urls import path, include
from django.contrib.auth.views import PasswordResetView

from wire.forms import PasswordResetForm


urlpatterns = [
    path(
        "password_reset/",
        PasswordResetView.as_view(form_class=PasswordResetForm),
        name="password_reset"
    ),
    path("", include("django.contrib.auth.urls"))
]
    
