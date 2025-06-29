def validate_slot(slot_name, value, diction_map):
    if slot_name not in diction_map:
        return False
    return value in diction_map[slot_name]
