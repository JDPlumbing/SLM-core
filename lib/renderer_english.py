import json

SLOT_ORDER = [
    "verb", "object", "location", "status", "goal", "cause", "evidence", "system",
    "tool", "material", "interface", "authority", "role", "timecode", "signature", "priority"
]

# Load SLM dictionaries
def load_dictionaries(path="diction"):
    dictionaries = {}
    for slot in SLOT_ORDER:
        try:
            with open(f"{path}/slm_{slot}_dictionary.json", "r") as f:
                dictionaries[slot] = {int(k, 16): v for k, v in json.load(f).items()}
        except FileNotFoundError:
            dictionaries[slot] = {}
    return dictionaries

# Render to human-readable English
def render_english(slots: dict, dictionaries: dict) -> str:
    pieces = []

    role = dictionaries["role"].get(slots.get("role", 0), "Someone")
    verb = dictionaries["verb"].get(slots.get("verb", 0), "did something to")
    obj = dictionaries["object"].get(slots.get("object", 0), "something")
    loc = dictionaries["location"].get(slots.get("location", 0), None)
    status = dictionaries["status"].get(slots.get("status", 0), None)
    goal = dictionaries["goal"].get(slots.get("goal", 0), None)

    sentence = f"{role} {verb} the {obj}"
    if loc: sentence += f" at the {loc}"
    if goal: sentence += f" to {goal}"
    if status: sentence += f", status: {status}"

    return sentence.strip()

# Example test block
# if __name__ == "__main__":
#     example = {
#         "verb": 3, "object": 4, "location": 2, "status": 71, "goal": 0,
#         "cause": 0, "evidence": 0, "system": 0, "tool": 0, "material": 0,
#         "interface": 7, "authority": 0, "role": 0, "timecode": 0,
#         "signature": 0, "priority": 0
#     }
#     dictionaries = load_dictionaries("diction")
#     print(render_english(example, dictionaries))

