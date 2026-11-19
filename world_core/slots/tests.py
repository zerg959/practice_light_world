import pytest
from slots.models import Slot, SlotHeight, SlotStatus, SlotWidth

@pytest.mark.django_db
class TestSlotModel:
    """
    Юнит-тесты класса Ячейка (Slot)
    """
    def test_slot_created_in_db(self, empty_slot):
        found = Slot.objects.filter(id=empty_slot.id).first()
        assert found is not None
        assert found.id == empty_slot.id
        assert found.slot_status == SlotStatus.EMPTY

    def test_slot_num_in_corr_range(self):
        pass

    def test_channel_num_in_corr_range(self):
        pass