from django.contrib import admin
from .models import Tariff


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("unit", "price_per_unit", "version", "is_active", "created_at")
    list_filter = ("unit", "is_active")
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        # если админ активировал тариф — деактивируем его конкурента
        if obj.is_active:
            Tariff.objects.filter(unit=obj.unit, is_active=True)\
                          .exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)
