from django.contrib import admin
from .models import Slot


@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("__str__", "slot_number", "width", "height",
                    "slot_status", "controller", "controller_channel_num")
    list_filter = ("slot_status", "controller")
    search_fields = ("slot_number",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("controller")
