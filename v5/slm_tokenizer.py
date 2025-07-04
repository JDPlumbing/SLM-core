import os

DICT_PATH = "dicts"
SLOTS = ["subject", "verb", "object", "modifier", "location", "intent", "cause", "status", "adverb"]

CLAUSE_JOINERS = {"so", "that", "then", "because", "and", "but"}
LOCATION_PREPOSITIONS = {"in", "on", "under", "at"}

def get_entries_by_slot():
    entries = {}
    for slot in SLOTS:
        path = os.path.join(DICT_PATH, f"{slot}.txt")
        if not os.path.exists(path):
            entries[slot] = set()
            continue
        with open(path) as f:
            entries[slot] = set(line.strip() for line in f if line.strip())
    return entries

def tokenize(text):
    words = text.strip().lower().replace(",", "").replace(".", "").split()
    PRONOUNS = {"i", "he", "she", "we", "they", "you"}
    words = [("someone" if w in PRONOUNS else w) for w in words]

    slots = get_entries_by_slot()

    clause_a = {slot: None for slot in SLOTS}
    clause_b = {slot: None for slot in SLOTS}
    clause = clause_a

    def assign(clause, slot, value):
        if clause[slot] is None:
            clause[slot] = value
            return True
        return False

    i = 0
    while i < len(words):
        token = words[i]
        next_token = words[i + 1] if i + 1 < len(words) else None
        third_token = words[i + 2] if i + 2 < len(words) else None
        pair = f"{token}_{next_token}" if next_token else None

        # Clause boundary check
        if token in CLAUSE_JOINERS:
            clause = clause_b
            i += 1
            continue

        # Location detection: preposition + article + noun (e.g. in the basement)
        if token in LOCATION_PREPOSITIONS and next_token and third_token:
            composite = f"{next_token}_{third_token}"  # e.g. the_basement
            if composite in slots["location"]:
                assign(clause, "location", composite)
                i += 3
                continue

        # Try 2-word pair first
        if pair:
            matched = False
            for slot in SLOTS:
                if pair in slots[slot]:
                    if assign(clause, slot, pair):
                        i += 2
                        matched = True
                        break
            if matched:
                continue

        # Try single token
        matched = False
        for slot in SLOTS:
            if token in slots[slot]:
                if assign(clause, slot, token):
                    matched = True
                    break

        # Fallback: modifier followed by object
        if matched and token in slots["modifier"] and next_token in slots["object"]:
            assign(clause, "object", next_token)
            i += 1
            continue

        # Fallback: someone_verb
        if not matched and clause["verb"] is None:
            if f"someone_{token}" in slots["verb"]:
                assign(clause, "verb", f"someone_{token}")

        i += 1

    # Final fallback: default subject
    if clause_a["subject"] is None and clause_a["verb"]:
        clause_a["subject"] = "someone"
    if clause_b["subject"] is None and clause_b["verb"]:
        clause_b["subject"] = "someone"

    # Final pass: sliding window for object resolution like "the loose valve"
    print("🧪 Sliding window object check:")
    for i in range(len(words)):
        if clause["object"] is not None:
            break
        if words[i] in {"the", "a", "an"}:
            for j in range(i + 1, min(i + 4, len(words))):
                candidate = f"{words[i]}_{words[j]}"
                print(f"  🔍 Checking: {candidate}")
                if candidate in slots["object"]:
                    print(f"  ✅ Matched object: {candidate}")
                    clause["object"] = candidate
                    break
            if clause["object"]:
                break

    return clause_a, clause_b
