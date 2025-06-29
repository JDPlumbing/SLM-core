from loader import load_dictionaries
from utils import bytes_to_int

def decode_tuple(byte_data, diction):
    result = {}
    idx = 0
    for slot in diction["slots"]:
        width = slot["bytes"]
        val_bytes = byte_data[idx:idx+width]
        result[slot["name"]] = bytes_to_int(val_bytes)
        idx += width
    return result
