import os
import json

SLOT_ORDER = [
    "verb", "object", "location", "status", "goal", "cause", "evidence", "system",
    "tool", "material", "interface", "authority", "role", "timecode", "signature", "priority"
]

def load_dictionaries(path="diction"):
    diction_map = {}
    diction = {}
    reverse_map = {}

    for slot in SLOT_ORDER:
        fname = f"slm_{slot}_dictionary.json"
        fpath = os.path.join(path, fname)

        try:
            with open(fpath, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        # Forward map: code → string
        diction_map[slot] = {int(k, 16): str(v).lower() for k, v in data.items()}
        # Basic list
        diction[slot] = [str(v).lower() for v in data.values()]
        # Reverse map: string → code
        reverse_map[slot] = {str(v).lower(): int(k, 16) for k, v in data.items() if v}

    return diction_map, diction, reverse_map




def load_meta(path="diction/_meta.json"):
    with open(path, "r") as f:
        return json.load(f)
