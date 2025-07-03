import os

DICT_PATH = "dicts"
SLOTS = ["subject", "verb", "object", "modifier", "location", "intent", "cause", "status", "adverb"]

# Load dictionary entries
slot_entries = {}
for slot in SLOTS:
    with open(os.path.join(DICT_PATH, f"{slot}.txt")) as f:
        slot_entries[slot] = set(line.strip() for line in f if line.strip())

def find_partial_match(word, entries):
    """Match word to the tail of compound entries like someone_installed"""
    for entry in entries:
        if "_" in entry:
            _, base = entry.split("_", 1)
            if word == base:
                return entry
    return None

def tokenize(text):
    words = text.strip().lower().replace(",", "").replace(".", "").split()
    clause_a = {slot: None for slot in SLOTS}
    clause_b = {slot: None for slot in SLOTS}
    i = 0

    def assign(slot, value):
        if clause_a[slot] is None:
            clause_a[slot] = value
        elif clause_b[slot] is None:
            clause_b[slot] = value

    while i < len(words):
        matched = False

        # Try 2-word combos
        if i + 1 < len(words):
            pair = f"{words[i]}_{words[i+1]}"
            for slot, entries in slot_entries.items():
                if pair in entries:
                    assign(slot, pair)
                    matched = True
                    i += 2
                    break

        if not matched:
            word = words[i]

            # Exact slot matches
            for slot in SLOTS:
                if word in slot_entries[slot]:
                    assign(slot, word)
                    matched = True
                    break

            # Adverb or modifier specific rules
            if not matched:
                if word.endswith("ly") and word in slot_entries["adverb"]:
                    assign("adverb", word)
                    matched = True
                elif word in slot_entries["modifier"]:
                    assign("modifier", word)
                    matched = True

            # Partial match (e.g. installed → someone_installed)
            if not matched:
                for slot in SLOTS:
                    entry = find_partial_match(word, slot_entries[slot])
                    if entry:
                        assign(slot, entry)
                        matched = True
                        break

            # Pronoun fallback
            if not matched and word in {"i", "you", "he", "she", "we", "they"}:
                assign("subject", word)

            i += 1

    # Fallbacks for clause A only
    if clause_a["subject"] is None:
        clause_a["subject"] = "someone"
    if clause_a["verb"] is None:
        clause_a["verb"] = "did_something"
    if clause_a["object"] is None:
        clause_a["object"] = "something"
    if clause_a["location"] is None:
        clause_a["location"] = "somewhere"
    if clause_a["adverb"] is None:
        clause_a["adverb"] = "somehow"

    return clause_a, clause_b
