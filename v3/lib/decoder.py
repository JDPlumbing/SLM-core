from encoder import SLOT_MANIFEST

def decode_bytecode(byte_data, dict_map):
    offset = 0
    result = {}
    for slot_name, byte_width in SLOT_MANIFEST:
        chunk = byte_data[offset:offset + byte_width]
        offset += byte_width

        if all(b == 0 for b in chunk):
            result[slot_name] = "<null>"
            continue

        hexcode = chunk.hex().lower().zfill(byte_width * 2)

        # Look up using .fwd dict (hex → word)
        word = dict_map[slot_name]["fwd"].get(hexcode)
        result[slot_name] = word
        

    return result
