from django.contrib import admin

from .models import HardwareCommand, SensorEvent


@admin.register(HardwareCommand)
class HardwareCommandAdmin(admin.ModelAdmin):
    list_display = (
        "command_type", "controller", "channel",
        "status", "created_at", "sent_at", "finished_at",
    )
    list_filter = ("status", "command_type", "controller")
    search_fields = ("id", "channel")
    readonly_fields = (
        "id", "status", "created_at", "sent_at", "finished_at",
    )
    ordering = ("-created_at",)
    list_per_page = 25

    fieldsets = (
        ("Команда", {
            "fields": ("id", "controller", "channel", "command_type"),
        }),
        ("Статус", {
            "fields": ("status", "created_at", "sent_at", "finished_at"),
        }),
    )


@admin.register(SensorEvent)
class SensorEventAdmin(admin.ModelAdmin):
    list_display = (
        "event_type", "controller", "channel",
        "processing_status", "attempts", "received_at",
    )
    list_filter = ("event_type", "processing_status", "controller")
    search_fields = ("id",)
    readonly_fields = (
        "id", "controller", "channel", "event_type", "raw_data",
        "received_at", "processed_at", "attempts",
    )
    ordering = ("-received_at",)
    list_per_page = 25

    fieldsets = (
        ("Событие", {
            "fields": ("id", "controller", "channel", "event_type"),
        }),
        ("Обработка", {
            "fields": (
                "processing_status", "processed_at",
                "processing_error", "attempts",
            ),
        }),
        ("Сырые данные", {
            "fields": ("raw_data", "received_at"),
        }),
    )
