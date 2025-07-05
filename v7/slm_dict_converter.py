# slm_tokenizer.py (Greedy, Deterministic — No spaCy)
import os
from typing import Dict, List, Tuple

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
                data[slot] = sorted(set(entries))
    return data

# --- Tokenizer ---
def tokenize(sentence: str, dicts: Dict[str, List[str]] = None) -> Tuple[Dict[str, str], Dict[str, str]]:
    if dicts is None:
        dicts = load_dictionaries()

    words = sentence.lower().split()
    used_indices = set()
    clause_a = {slot: None for slot in SLOTS}
    clause_b = {slot: None for slot in SLOTS}

    # Fill Clause
    def fill_clause(matches: Dict[str, str], used: set, words: List[str]):
        # Pass 1: Two-word combos, match against single-prefixed entries
        for i in range(len(words) - 1):
            if i in used or i+1 in used:
                continue
            pair = f"{words[i]}_{words[i+1]}"
            for slot in SLOTS:
                if matches[slot] is None:
                    single_prefix = PREFIXES[slot][0]
                    entry = f"{single_prefix}{pair}"
                    if entry in dicts.get(slot, []):
                        matches[slot] = entry
                        used.update([i, i+1])
                        break

        # Pass 2: One-word matches, against double-prefixed entries
        for i, word in enumerate(words):
            if i in used:
                continue
            for slot in SLOTS:
                if matches[slot] is None:
                    double_prefix = PREFIXES[slot][1]
                    entry = f"{double_prefix}{word}"
                    if entry in dicts.get(slot, []):
                        matches[slot] = entry
                        used.add(i)
                        break

        return matches, used

    clause_a, used_indices = fill_clause(clause_a, used_indices, words)
    clause_b, _ = fill_clause(clause_b, used_indices.copy(), words)

    if clause_a["subject"] is None:
        clause_a["subject"] = "!!someone"

    return clause_a, clause_b

# --- CLI Hook ---
if __name__ == "__main__":
    dicts = load_dictionaries()
    while True:
        try:
            sent = input("Say something: ").strip()
            if sent.lower() in ["exit", "quit"]:
                break
            a, b = tokenize(sent, dicts)
            print("\n\U0001F4E6 Clause A:")
            print(a)
            print("\n\U0001F4E6 Clause B:")
            print(b)
            print("\n\U0001F4BE Raw Match:")
            print(" ".join([v for v in a.values() if v] + [v for v in b.values() if v]))
            print("-" * 40)
        except KeyboardInterrupt:
            break

"""
README — SLM Tokenizer v7
=========================

This tokenizer parses natural language into structured SLM slot entries for downstream use. It is fully deterministic, greedy (left-to-right), and prefix-driven. No NLP or dependency trees. Just clean matching.

Slot Schema:
------------
- subject
- verb
- object
- location
- intent
- cause
- status
- adverb

Prefix Rules:
-------------
- **Single-symbol prefixes** (`!`, `#`, `~`, etc.) are used **only for 2-word entries** like `!water_heater` or `~did_replace`
- **Double-symbol prefixes** (`!!`, `##`, `~~`, etc.) are used **only for 1-word entries** like `!!plumber` or `##dishwasher`

Tokenizer Logic:
----------------
1. **Clause A pass 1**: scan for 2-word matches (e.g. `water_heater`) and match against single-symbol prefixed dictionary entries (e.g. `#water_heater`)
2. **Clause A pass 2**: scan remaining orphan words and match against double-symbol entries (e.g. `##heater`)
3. **Clause B**: repeat steps 1 & 2 using remaining words
4. **Subject fallback**: if no subject is matched in Clause A, defaults to `!!someone`

Dictionaries:
-------------
- Stored in `/dicts/{slot}.txt`
- Each entry must start with the correct prefix
- Do **not** mix single and double prefix styles — enforce prefix rules above

Example:
--------
Sentence:
    "The plumber did fix the rusty pipe to address the leak"

Output:
    !!plumber ~did_fix #rusty_pipe >to_address <<leak

That’s your full raw match, machine-readable and human-legible.

Use Cases:
----------
- Translating job logs
- Building chaincode capsules
- Structured tagging of task and action data
"""
