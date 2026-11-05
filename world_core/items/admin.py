from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "current_slot", "weight",
                    "width", "height", "created_at")
    list_filter = ("status",)
    search_fields = ("name",)
    readonly_fields = ("created_at",)
