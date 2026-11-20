from datetime import timedelta
from django.utils import timezone

RENTAL_START = timezone.make_aware(
    timezone.datetime(2026, 10, 15, 10, 0, 0)
)
RENTAL_FINISH = RENTAL_START + timedelta(hours=2)
RENTAL_HOURS = 2