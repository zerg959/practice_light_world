# Проверка «предмет влезает в ячейку» (width/height против габаритов слота).
# item.current_slot и slot.slot_status меняются всегда в одной транзакции и всегда вместе
# положили предмет в ячейку B: item.current_slot = B, item.status = 'available', slot_B.slot_status = 'busy';
# забрали на старте аренды: item.current_slot = None, item.status = 'rented', slot_A.slot_status = 'empty'.