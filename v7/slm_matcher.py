# slm_matcher.py (v7, strict)
import os
import re
from typing import Dict, Set, List, Tuple

DICT_PATH = "dicts"

PREFIX_TO_SLOT = {
    "!": "subject",
    "#": "object",
    "@": "location",
    "~": "verb",
    ">": "intent",
    "<": "cause",
    ":": "status",
    "-": "adverb"
}

# Strict match: ONLY two-word entries, enforced by prefix + underscore
STRICT_WILDCARD_PATTERN = re.compile(r"^([!#@~><:\-]{2})_(\w+)$")
STRICT_SPECIFIC_PATTERN = re.compile(r"^([!#@~><:\-])([a-z]+_[a-z]+)$")

def load_prefixed_slot_dicts(dict_path: str = DICT_PATH) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    tier1 = {slot: set() for slot in PREFIX_TO_SLOT.values()}
    tier2 = {slot: set() for slot in PREFIX_TO_SLOT.values()}

    if not os.path.exists(dict_path):
        return tier1, tier2

    for filename in os.listdir(dict_path):
        if not filename.endswith(".txt"):
            continue
        full_path = os.path.join(dict_path, filename)
        with open(full_path, "r", encoding="utf-8") as f:
            for line in f:
                token = line.strip()
                if not token or "_" not in token:
                    continue
                if STRICT_SPECIFIC_PATTERN.match(token):
                    prefix, _ = STRICT_SPECIFIC_PATTERN.match(token).groups()
                    slot = PREFIX_TO_SLOT.get(prefix)
                    if slot:
                        tier1[slot].add(token)
                elif STRICT_WILDCARD_PATTERN.match(token):
                    prefix, _ = STRICT_WILDCARD_PATTERN.match(token).groups()
                    slot = PREFIX_TO_SLOT.get(prefix[0])
                    if slot:
                        tier2[slot].add(token)

    return tier1, tier2

def match_token_to_slot(token: str, tier1: Dict[str, Set[str]], tier2: Dict[str, Set[str]]) -> Tuple[str, str]:
    # Only match full tokens from tier1 (two-word only)
    for slot, entries in tier1.items():
        for entry in entries:
            if entry.endswith(f"_{token}") or entry == token:
                return (slot, entry)
    # Then allow suffix match for tier2 wildcards
    for slot, entries in tier2.items():
        for entry in entries:
            if entry.endswith(f"_{token}"):
                return (slot, entry)
    return ("unknown", token)

def batch_match_tokens(tokens: List[str], tier1: Dict[str, Set[str]], tier2: Dict[str, Set[str]]) -> List[Tuple[str, str]]:
    results = []
    for token in tokens:
        slot, value = match_token_to_slot(token, tier1, tier2)
        if slot != "unknown":
            results.append((slot, value))
    return results