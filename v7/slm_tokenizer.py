# slm_tokenizer.py (Greedy, Deterministic — No spaCy)
import os
import re
from typing import Dict, List

SLOTS = ["subject", "verb", "object", "location", "intent", "cause", "status", "adverb"]
PREFIXES = {
    "subject": ["!", "!!"],
    "verb": ["~", "~~"],
    "object": ["#", "##"],
    "location": ["@", "@@"],
    "intent": [">", ">>"],
    "cause": ["<", "<<"],
    "status": [":", "::"],
    "adverb": ["-", "--"]
}

# --- Dict Loader ---
def load_dictionaries(dict_path="dicts") -> Dict[str, List[str]]:
    data = {}
    for slot in SLOTS:
        slot_file = os.path.join(dict_path, f"{slot}.txt")
        if os.path.exists(slot_file):
            with open(slot_file, encoding="utf-8") as f:
                entries = [line.strip() for line in f if line.strip()]
                # Strip symbols and leading underscores for matching
                data[slot] = sorted(set([normalize_token(entry) for entry in entries]))
    return data

def strip_prefix(token: str) -> str:
    # Remove up to two leading prefix characters
    while token and token[0] in "!#@~><:-":
        token = token[1:]
    return token

def normalize_token(token: str) -> str:
    token = strip_prefix(token)
    return token[1:] if token.startswith("_") else token

# --- Tokenizer ---
def tokenize(sentence: str, dicts: Dict[str, List[str]] = None):
    if dicts is None:
        dicts = load_dictionaries()

    sentence = re.sub(r"[^\w\s]", "", sentence.lower())
    words = sentence.split()
    used_indices = set()

    def fill_clause(word_list, exclude_indices):
        clause = {slot: None for slot in SLOTS}
        used = set()

        # First Pass: 2-word combos
        for i in range(len(word_list) - 1):
            if i in exclude_indices or i+1 in exclude_indices:
                continue
            pair = f"{word_list[i]}_{word_list[i+1]}"
            for slot in SLOTS:
                if clause[slot] is None and pair in dicts.get(slot, []):
                    clause[slot] = prefix_token(slot, pair)
                    used.update([i, i+1])
                    break

        # Second Pass: single word orphans
        for i, word in enumerate(word_list):
            if i in exclude_indices or i in used:
                continue
            for slot in SLOTS:
                if clause[slot] is None and word in dicts.get(slot, []):
                    clause[slot] = prefix_token(slot, word)
                    used.add(i)
                    break

        # Subject fallback
        if clause["subject"] is None:
            clause["subject"] = "!!_someone"

        return clause, used

    # Fill Clause A
    clause_a, used_a = fill_clause(words, exclude_indices=used_indices)

    # Fill Clause B using leftovers
    leftover_words = [w for i, w in enumerate(words) if i not in used_a]
    clause_b, _ = fill_clause(leftover_words, exclude_indices=set())

    return clause_a, clause_b

    if dicts is None:
        dicts = load_dictionaries()

    sentence = re.sub(r"[^\w\s]", "", sentence.lower())
    words = sentence.split()
    used_indices = set()
    matches = {slot: None for slot in SLOTS}

    # First Pass: Exact 2-word matches (greedy left to right)
    for i in range(len(words) - 1):
        pair = f"{words[i]}_{words[i+1]}"
        for slot in SLOTS:
            if matches[slot] is None and pair in dicts.get(slot, []):
                matches[slot] = prefix_token(slot, pair)
                used_indices.update([i, i+1])
                break

    # Second Pass: Orphan single word matches (slot must be still empty)
    for i, word in enumerate(words):
        if i in used_indices:
            continue
        for slot in SLOTS:
            if matches[slot] is None and word in dicts.get(slot, []):
                matches[slot] = prefix_token(slot, word)
                used_indices.add(i)
                break

    # Subject fallback
    if matches["subject"] is None:
        matches["subject"] = "!!_someone"

    return matches

# --- Utility ---
def prefix_token(slot: str, token: str) -> str:
    prefix = PREFIXES[slot][0] if token.count("_") == 1 else PREFIXES[slot][1]
    return f"{prefix}{token}"

# --- CLI Hook ---
if __name__ == "__main__":
    dicts = load_dictionaries()
    while True:
        try:
            sent = input("Say something: ").strip()
            if sent.lower() in ["exit", "quit"]:
                break
            result = tokenize(sent, dicts)
            for slot, val in result.items():
                print(f"{slot}: {val}")
        except KeyboardInterrupt:
            break
