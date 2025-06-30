import json
import os

DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dict"))

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
    "spaces": "space",
    "intents": "intent"
    
}

def load_dictionaries():
    dict_map = {}
    for fname in os.listdir(DICT_DIR):
        if fname.endswith(".json"):
            slot_name = fname[:-5]  # strip ".json"
            with open(os.path.join(DICT_DIR, fname), 'r') as f:
                data = json.load(f)
            # Load verb dict from JSON
            forward = {k.lower(): v.lower() for k, v in data.items()} 
            reverse = {v.lower(): k.lower() for k, v in data.items()}

            slot_key = DICT_SLOT_MAP.get(slot_name, slot_name)
            dict_map[slot_key] = {
                "fwd": forward,
                "rev": reverse
            }
    return dict_map
