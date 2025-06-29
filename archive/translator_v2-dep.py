import os
import json
import difflib
from typing import Dict

SLOT_ORDER = [
    "verb", "object", "location", "status", "goal", "cause", "evidence", "system",
    "tool", "material", "interface", "authority", "role", "timecode", "signature", "priority"
]

# Normalize individual token (basic lemmatization)
def normalize_token(token):
    token = token.lower()
    for suffix in ['ing', 'ed', 'es', 's']:
        if token.endswith(suffix) and len(token) > len(suffix) + 1:
            token = token[:-len(suffix)]
            break
    return token

# Load dictionaries and build forward + reverse maps
def load_all_dictionaries(path="diction"):
    dictionaries = {}
    reverse_maps = {}
    for fname in os.listdir(path):
        if fname.endswith("_dictionary.json"):
            key = fname.replace("slm_", "").replace("_dictionary.json", "")
            with open(os.path.join(path, fname), "r") as f:
                data = json.load(f)

            # Forward: int → string (lowercased)
            dictionaries[key] = {int(k, 16): v.lower() for k, v in data.items()}
            # Reverse: normalized string → int
            reverse_maps[key] = {
                normalize_token(str(v)): int(k, 16)
                for k, v in data.items() if v
            }

    return dictionaries, reverse_maps

# Fuzzy match input tokens to dictionary entries
def parse_input(text: str, reverse_maps: Dict[str, Dict[str, int]], cutoff=0.85) -> Dict[str, int]:
    result = {}
    text = str(text).lower()
    tokens = [normalize_token(t) for t in text.replace(",", "").split()]

    for slot, str_to_code in reverse_maps.items():
        keys = list(str_to_code.keys())
        match = None
        for token in tokens:
            found = difflib.get_close_matches(token, keys, n=1, cutoff=cutoff)
            if found:
                match = found[0]
                break
        if match:
            result[slot] = str_to_code[match]

    return result

# Normalize to full 16-slot structure with 0 fallback
def normalize_slots(parsed: Dict[str, int], slot_order=SLOT_ORDER) -> Dict[str, int]:
    return {slot: parsed.get(slot, 0x0000) for slot in slot_order}

# Render machine tuple to readable string
def render_structured(slots: Dict[str, int], dictionaries: Dict[str, Dict[int, str]]) -> str:
    readable = []
    for slot in SLOT_ORDER:
        val = slots.get(slot, 0x0000)
        term = dictionaries.get(slot, {}).get(val, f"<0x{val:04X}>")
        readable.append(f"{slot}: {term}")
    return " | ".join(readable)

# CLI test mode
if __name__ == "__main__":
    dictionaries, reverse_maps = load_all_dictionaries(path="diction")
    print("SLM Translator (v2): Type your input (or 'exit'):")
    while True:
        text = input("> ")
        if text.strip().lower() in ["exit", "quit"]:
            break
        parsed = parse_input(text, reverse_maps)
        normalized = normalize_slots(parsed)
        rendered = render_structured(normalized, dictionaries)

        print("\nParsed:")
        for k, v in parsed.items():
            print(f"  {k}: 0x{v:04X}")

        print("\nNormalized Tuple:")
        for k in SLOT_ORDER:
            print(f"  {k}: 0x{normalized[k]:04X}")

        print("\nStructured:")
        print(rendered)
        print("-" * 40)
