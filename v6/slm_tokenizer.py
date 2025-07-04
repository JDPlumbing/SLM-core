import os

DICT_PATH = "dicts"
SLOTS = ["subject", "verb", "object", "location", "intent", "cause", "status", "adverb"]

CLAUSE_JOINERS = {"so", "that", "then", "because"}
LOCATION_PREPOSITIONS = {"in", "on", "under", "at"}
PRONOUNS = {"i", "he", "she", "we", "they", "you"}

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
    words = ["someone" if w in PRONOUNS else w for w in words]

    slots = get_entries_by_slot()
    clause_a = {slot: None for slot in SLOTS}
    clause_b = {slot: None for slot in SLOTS}
    clause = clause_a

    # 🔧 Inject implied subject if first word is verb root
    if words:
        first = words[0]
        if f"someone_{first}" in slots["verb"]:
            words = [f"someone_{first}"] + words[1:]

    def assign(clause, slot, value):
        if clause[slot] is None:
            clause[slot] = value
            return True
        return False

    i = 0
    while i < len(words):
        token = words[i]
        next_token = words[i + 1] if i + 1 < len(words) else None
        pair = f"{token}_{next_token}" if next_token else None

        if token in CLAUSE_JOINERS:
            clause = clause_b
            i += 1
            continue

        if token in LOCATION_PREPOSITIONS and next_token in slots["location"]:
            if assign(clause, "location", next_token) or assign(clause_b, "location", next_token):
                i += 2
                continue

        if pair:
            matched = False
            for slot in SLOTS:
                if pair in slots[slot]:
                    if assign(clause, slot, pair) or assign(clause_b, slot, pair):
                        matched = True
                        break
            if matched:
                i += 1
                continue

        matched = False
        for slot in SLOTS:
            if token in slots[slot]:
                if assign(clause, slot, token) or assign(clause_b, slot, token):
                    matched = True
                    break
        i += 1

    return clause_a, clause_b
