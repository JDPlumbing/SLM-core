import os

DICT_PATH = "dicts"
SLOTS = ["subject", "verb", "object", "modifier", "location", "intent", "cause", "status", "adverb"]

CLAUSE_JOINERS = {"so", "that", "then", "because"}
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
        pair = f"{token}_{next_token}" if next_token else None

        # Clause boundary check
        if token in CLAUSE_JOINERS:
            clause = clause_b
            i += 1
            continue

        # Location detection: preposition + known location noun
        if token in LOCATION_PREPOSITIONS and next_token in slots["location"]:
            assign(clause, "location", next_token)
            i += 2
            continue

        # Subject early-catch: pronoun or dict match
        if clause["subject"] is None:
            if token in {"i", "he", "she", "they", "we", "you"} or token in slots["subject"]:
                assign(clause, "subject", token)
                i += 1
                continue

        # Try 2-word pair first (e.g. he_is, is_running)
        if pair:
            for slot in SLOTS:
                if pair in slots[slot]:
                    if assign(clause, slot, pair):
                        i += 2
                        break
            else:
                # No match for pair, try single
                matched = False
                for slot in SLOTS:
                    if token in slots[slot]:
                        if assign(clause, slot, token):
                            matched = True
                            break
                if not matched:
                    i += 1
        else:
            # Final word, try single match
            for slot in SLOTS:
                if token in slots[slot]:
                    assign(clause, slot, token)
                    break
            i += 1

    return clause_a, clause_b
