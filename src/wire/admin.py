from django.contrib import admin
from wire.models import WireLog


@admin.register(WireLog)
class WireLogAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "sub_label", "created")
    list_filter = ("label",)
    ordering = ("-created",)
