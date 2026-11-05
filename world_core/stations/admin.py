from django.contrib import admin
from .models import Station, StationConfig, Controller


class ControllerInline(admin.TabularInline):
    model = Controller
    extra = 0
    fields = ("name", "serial_number", "status", "last_seen_at")
    readonly_fields = ("status", "last_seen_at")


class StationConfigInline(admin.TabularInline):
    model = StationConfig
    extra = 0
    readonly_fields = ("created_at",)
    fields = ("version_number", "status", "snapshot", "created_at")


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ("id", "station_status", "location",
                    "current_applied_config_version")
    list_filter = ("station_status",)
    search_fields = ("location",)
    inlines = (ControllerInline, StationConfigInline)


@admin.register(Controller)
class ControllerAdmin(admin.ModelAdmin):
    list_display = ("serial_number", "name", "station", "status", "last_seen_at")
    list_filter = ("status", "station")
    search_fields = ("serial_number", "name")
    readonly_fields = ("status", "last_seen_at", "created_at")


@admin.register(StationConfig)
class StationConfigAdmin(admin.ModelAdmin):
    list_display = ("station", "version_number", "status", "created_at", "created_by")
    list_filter = ("status", "station")
    readonly_fields = ("created_at",)

