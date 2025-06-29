from encode import encode_tuple
from decode import decode_tuple
from loader import load_dictionaries, load_meta

def main():
    diction_map, _ = load_dictionaries()
    meta = load_meta()
    slot_values = {slot["name"]: int(input(f"{slot['name']} (0x): "), 16) for slot in meta["slots"]}
    encoded = encode_tuple(slot_values, meta)
    print("Encoded (hex):", encoded.hex())
    decoded = decode_tuple(encoded, meta)
    print("Decoded:", decoded)

if __name__ == "__main__":
    main()
