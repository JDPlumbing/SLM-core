# Full parser patch: this includes a clean tokenizer and clause assignment function,
# with fallback logic for clause A, and no clause-switching.

import os

DICT_PATH = "dicts"
SLOTS = ["subject", "verb", "object", "modifier", "location", "intent", "cause", "status", "adverb"]

# Load slot dictionary entries into memory
slot_entries = {}
for slot in SLOTS:
    path = os.path.join(DICT_PATH, f"{slot}.txt")
    if os.path.exists(path):
        with open(path) as f:
            slot_entries[slot] = set(line.strip() for line in f if line.strip())
    else:
        slot_entries[slot] = set()

def find_partial_match(word, entries):
    """Try to find entry where word matches the second half (e.g., 'install' in 'to_install')"""
    for entry in entries:
        if "_" in entry:
            _, base = entry.split("_", 1)
            if word == base:
                return entry
    return None

def tokenize(text):
    words = text.strip().lower().replace(",", "").replace(".", "").split()
    tokens = []
    i = 0

    while i < len(words):
        if i + 1 < len(words):
            pair = f"{words[i]}_{words[i+1]}"
            for slot, entries in slot_entries.items():
                if pair in entries:
                    tokens.append((slot, pair))
                    i += 2
                    break
            else:
                word = words[i]
                if word.endswith("ly") and word in slot_entries["adverb"]:
                    tokens.append(("adverb", word))
                elif word in slot_entries["modifier"]:
                    tokens.append(("modifier", word))
                else:
                    matched = False
                    for slot in SLOTS:
                        if slot in ["modifier", "adverb"]:
                            continue
                        entry = find_partial_match(word, slot_entries[slot])
                        if entry:
                            tokens.append((slot, entry))
                            matched = True
                            break
                    if not matched:
                        tokens.append(("unknown", word))
                i += 1
        else:
            word = words[i]
            if word.endswith("ly") and word in slot_entries["adverb"]:
                tokens.append(("adverb", word))
            elif word in slot_entries["modifier"]:
                tokens.append(("modifier", word))
            else:
                matched = False
                for slot in SLOTS:
                    if slot in ["modifier", "adverb"]:
                        continue
                    entry = find_partial_match(word, slot_entries[slot])
                    if entry:
                        tokens.append((slot, entry))
                        matched = True
                        break
                if not matched:
                    tokens.append(("unknown", word))
            i += 1
    return tokens

def assign_to_clauses(tokens):
    clause_a = {slot: None for slot in SLOTS}
    clause_b = {slot: None for slot in SLOTS}

    for slot, value in tokens:
        if slot in clause_a and clause_a[slot] is None:
            clause_a[slot] = value

    # Apply fallback defaults to Clause A
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

