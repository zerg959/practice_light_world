from django.contrib import admin
from .models import Rental, RentalEvent


class RentalEventInline(admin.TabularInline):
    model = RentalEvent
    extra = 0
    can_delete = False
    fields = ("type", "started_at", "finished_at",
              "price_per_unit", "unit", "total_amount", "created_at")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item", "rental_status",
                    "rental_start", "rental_finish",
                    "start_slot", "finish_slot")
    list_filter = ("rental_status", "rental_unit")
    search_fields = ("user__username", "item__name")
    # readonly_fields = ("created_at",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            "user", "item", "tariff", "start_station", "start_slot",
            "finish_station", "finish_slot",
        )


@admin.register(RentalEvent)
class RentalEventAdmin(admin.ModelAdmin):
    list_display = ("rental", "type", "started_at", "finished_at", "total_amount")
    list_filter = ("type",)
    search_fields = ("rental__id",)
    ordering = ("-started_at",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
