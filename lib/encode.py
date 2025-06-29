from loader import load_dictionaries
from utils import int_to_bytes

def encode_tuple(slot_values, diction):
    block = bytearray()
    for slot in diction["slots"]:
        value = slot_values.get(slot["name"], 0)
        block += int_to_bytes(value, slot["bytes"])
    return block
