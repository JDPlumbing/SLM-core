# v3/lib/slm_tokenizer.py

import os
import json
from collections import defaultdict
from slm_normalizer import normalize_tokens  # <- added this line

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dict"))

# Load all slot dictionaries into memory
slot_dicts = {}
for fname in os.listdir(DICT_DIR):
    if fname.endswith(".json"):
        slot = fname[:-5]  # strip .json
        with open(os.path.join(DICT_DIR, fname), 'r') as f:
            data = json.load(f)
            reverse_map = {v.lower(): k for k, v in data.items()}  # lowercase
            slot_dicts[slot] = reverse_map

# Optional priority if collisions: check verbs before objects, etc
SLOT_PRIORITY = [
    "verbs", "objects", "subjects", "adjectives", "adverbs",
    "sizes", "materials", "shapes", "colors", "conditions",
    "purposes", "prepositions", "statuses", "causes", "intents", "spaces"
]

# Normalize dict names to encoder slot names
DICT_SLOT_MAP = {
    "verbs": "verb",
    "objects": "object",
    "subjects": "subject",
    "sizes": "size",
    "materials": "material",
    "shapes": "shape",
    "colors": "color",
    "conditions": "condition",
    "purposes": "purpose",
    "prepositions": "preposition",
    "adjectives": "adjective",
    "adverbs": "adverb",
    "statuses": "status",
    "causes": "cause",
    "intents": "intent",
    "spaces": "space"
}

# Precompute known terms for fuzzy matching
ALL_KNOWN_TERMS = set()
for d in slot_dicts.values():
    ALL_KNOWN_TERMS.update(d.keys())

def match_slots(raw_text):
    raw_tokens = raw_text.lower().replace('-', ' ').split()
    tokens = normalize_tokens(raw_text, ALL_KNOWN_TERMS)  # use normalizer first

    matched = {}
    for token in tokens:
        for dict_name in SLOT_PRIORITY:
            if token in slot_dicts.get(dict_name, {}):
                slot_name = DICT_SLOT_MAP[dict_name]
                if slot_name not in matched:
                    matched[slot_name] = token
                else:
                    # 🧠 Secondary fallback matchesinstal
                    if slot_name == "object":
                        if "cause" not in matched and token in slot_dicts.get("causes", {}):
                            matched["cause"] = token
                        elif "intent" not in matched and token in slot_dicts.get("intents", {}):
                            matched["intent"] = token
                    elif slot_name == "status":
                        if "adjective" not in matched and token in slot_dicts.get("adjectives", {}):
                            matched["adjective"] = token
                    elif slot_name == "verb":
                        if "intent" not in matched and token in slot_dicts.get("intents", {}):
                            matched["intent"] = token
                break
    return matched


if __name__ == "__main__":
    print("\n🧠 SLM Tokenizer")
    print("Type raw input like: 'ran to the store' or 'installed red toilet'\n")
    while True:
        raw = input(">>> ")
        if raw.strip().lower() in ('q', 'quit', 'exit'):
            break
        print(json.dumps(match_slots(raw), indent=2))
