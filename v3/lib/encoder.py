# v3/lib/encoder.py
SLOT_MANIFEST = [
    ("verb", 3),
    ("object", 3),
    ("subject", 2),
    ("size", 2),
    ("material", 2),
    ("shape", 2),
    ("color", 1),
    ("condition", 1),
    ("purpose", 2),
    ("preposition", 1),
    ("adjective", 2),
    ("adverb", 2),
    ("status", 1),
    ("cause", 3),
    ("intent", 3),
    ("space", 2)
]

def encode_slot_dict(slot_dict, dict_map):
    result = bytearray()
    for slot_name, byte_width in SLOT_MANIFEST:
        value = slot_dict.get(slot_name)
        if not value:
            result.extend(b"\x00" * byte_width)
            continue
        hexcode = dict_map[slot_name]["rev"].get(value.lower())
        if not hexcode:
            raise ValueError(f"Unknown word '{value}' in slot '{slot_name}'")
        result.extend(int(hexcode, 16).to_bytes(byte_width, "big"))
    return result

