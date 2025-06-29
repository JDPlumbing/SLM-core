import os
import json
import difflib
from typing import Dict

STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "to", "with", "from", "for",
    "of", "by", "and", "or", "as", "is", "was", "were", "be"
}

AUTO_ADD_SLOTS = {"object", "location", "tool", "material"}

SLOT_ORDER = [
    "verb", "object", "location", "status", "goal", "cause", "evidence", "system",
    "tool", "material", "interface", "authority", "role", "timecode", "signature", "priority"
]

def normalize_token(token):
    token = token.lower()
    for suffix in ['ing', 'ed', 'es', 's']:
        if token.endswith(suffix) and len(token) > len(suffix) + 1:
            token = token[:-len(suffix)]
            break
    return token

def load_all_dictionaries(path="diction"):
    dictionaries = {}
    reverse_maps = {}
    file_paths = {}
    for fname in os.listdir(path):
        if fname.endswith("_dictionary.json"):
            key = fname.replace("slm_", "").replace("_dictionary.json", "")
            full_path = os.path.join(path, fname)
            with open(full_path, "r") as f:
                data = json.load(f)
            dictionaries[key] = {int(k, 16): v.lower() for k, v in data.items()}
            reverse_maps[key] = {v.lower(): int(k, 16) for k, v in data.items()}
            file_paths[key] = full_path
    return dictionaries, reverse_maps, file_paths

def parse_input(text: str, reverse_maps: Dict[str, Dict[str, int]], dictionaries: Dict[str, Dict[int, str]], file_paths: Dict[str, str], cutoff=0.85) -> Dict[str, int]:
    result = {}
    text = str(text).lower()
    tokens = [normalize_token(t) for t in text.replace(",", "").split() if t.lower() not in STOPWORDS]

    used_tokens = set()

    for slot, str_to_code in reverse_maps.items():
        keys = list(str_to_code.keys())
        match = None
        for token in tokens:
            if token in used_tokens:
                continue
            found = difflib.get_close_matches(token, keys, n=1, cutoff=cutoff)
            if found:
                match = found[0]
                result[slot] = str_to_code[match]
                used_tokens.add(token)
                break

        if not match and slot in AUTO_ADD_SLOTS:
            for token in tokens:
                if token in used_tokens or token in str_to_code:
                    continue
                used_codes = set(dictionaries[slot].keys())
                next_code = max(used_codes) + 1 if used_codes else 1
                str_to_code[token] = next_code
                dictionaries[slot][next_code] = token
                result[slot] = next_code
                updated_dict = {f"{k:#06x}": v for k, v in dictionaries[slot].items()}
                with open(file_paths[slot], "w") as f:
                    json.dump(updated_dict, f, indent=2)
                used_tokens.add(token)
                break
    return result

def normalize_slots(parsed: Dict[str, int], slot_order=SLOT_ORDER) -> Dict[str, int]:
    return {slot: parsed.get(slot, 0x0000) for slot in slot_order}

def render_structured(slots: Dict[str, int], dictionaries: Dict[str, Dict[int, str]]) -> str:
    readable = []
    for slot in SLOT_ORDER:
        val = slots.get(slot, 0x0000)
        term = dictionaries.get(slot, {}).get(val, f"<0x{val:04X}>")
        readable.append(f"{slot}: {term}")
    return " | ".join(readable)
