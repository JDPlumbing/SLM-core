import os
import json
import difflib
from typing import Dict

# Load dictionaries
def load_all_dictionaries(path="diction"):
    dictionaries = {}
    reverse_maps = {}
    for fname in os.listdir(path):
        if fname.endswith("_dictionary.json"):
            key = fname.replace("slm_", "").replace("_dictionary.json", "")
            with open(os.path.join(path, fname), "r") as f:
                data = json.load(f)
            dictionaries[key] = {int(k, 16): v.lower() for k, v in data.items()}
            reverse_maps[key] = {v.lower(): int(k, 16) for k, v in data.items()}
    return dictionaries, reverse_maps

# Fuzzy parse human input to slot values
def parse_input(text: str, reverse_maps: Dict[str, Dict[str, int]], cutoff=0.85) -> Dict[str, int]:
    result = {}
    tokens = text.lower().replace(",", "").split()
    for slot, values in reverse_maps.items():
        keys = list(values.keys())
        match = difflib.get_close_matches(text, keys, n=1, cutoff=cutoff)
        if not match:
            for token in tokens:
                match = difflib.get_close_matches(token, keys, n=1, cutoff=cutoff)
                if match:
                    break
        if match:
            result[slot] = values[match[0]]
    return result

# Render structured values back into text
def render_structured(slots: Dict[str, int], dictionaries: Dict[str, Dict[int, str]]) -> str:
    readable = []
    for slot, val in slots.items():
        term = dictionaries.get(slot, {}).get(val, f"<0x{val:04X}>")
        readable.append(f"{slot}: {term}")
    return " | ".join(readable)

# Command-line test tool
if __name__ == "__main__":
    dictionaries, reverse_maps = load_all_dictionaries(path="diction")
    print("SLM Translator: Type your input (or 'exit'):")
    while True:
        text = input("> ")
        if text.strip().lower() in ["exit", "quit"]:
            break
        parsed = parse_input(text, reverse_maps)
        rendered = render_structured(parsed, dictionaries)
        print("Parsed:", parsed)
        print("Structured:", rendered)
