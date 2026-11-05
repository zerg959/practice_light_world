from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Tariff(models.Model):
    """
    Модель Тариф.
    Тариф описывает цену за единицу времени аренды.
    При старте аренды сервис копирует цифры в Rental (снапшот),
    поэтому изменение тарифа не задним числом меняет старые аренды.
    Важно:
    Constaints в Meta:
    1.Версия уникальна внутри единицы
    2.На каждую единицу — только один действующий тариф
    """

    class TariffUnit(models.TextChoices):
        HOUR = ('hour', 'Час')
        DAY = ('day', 'Сутки')
        MONTH = ('month', 'Месяц')

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="UUID",
        help_text="Уникальный ID тарифа",
    )
    unit = models.CharField(
        max_length=15,
        choices=TariffUnit.choices,
        verbose_name="Единица времени аренды",
        help_text="За что берётся плата: час, сутки, месяц",
    )
    price_per_unit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(
            Decimal("0.01"),
            message="Ставка аренды не может быть меньше 0.01",
        )],
        verbose_name="Цена за единицу",
        help_text="Сумма за одну единицу времени аренды",
    )
    version = models.CharField(
        max_length=30,
        verbose_name="Версия тарифа",
        help_text="Имя редакции тарифа, например «2026-весна»",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Действующий",
        help_text="Активен один тариф на единицу; старые версии отключаются",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан",
        help_text="Момент создания записи",
    )

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
        ordering = ["unit", "-created_at"]
        constraints = [
            # Версия уникальна внутри единицы
            models.UniqueConstraint(
                fields=["unit", "version"],
                name="tariff_unit_version_unique",
            ),
            # На каждую единицу — только один действующий тариф
            models.UniqueConstraint(
                fields=["unit"],
                condition=models.Q(is_active=True),
                name="tariff_one_active_per_unit",
            ),
        ]

    def __str__(self):
        mark = " ✓" if self.is_active else ""
        return f"{self.unit} — {self.price_per_unit} (v. {self.version}){mark}"
