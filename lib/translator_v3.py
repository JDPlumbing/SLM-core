import difflib
import json
from typing import List, Dict, Tuple

# Type Aliases
TokenList = List[str]
SlotDict = Dict[str, Dict[int, str]]         # Forward: hex -> label
ReverseDict = Dict[str, Dict[str, int]]      # Reverse: label -> hex
FilePaths = Dict[str, str]                   # Slot -> path
ResultTuple = Dict[str, int]

SLOT_ORDER = [
    "verb", "object", "location", "status", "goal", "cause", "evidence", "system",
    "tool", "material", "interface", "authority", "role", "timecode", "signature", "priority"
]

AUTO_ADD_SLOTS = {"object", "location", "tool", "material"}

STOPWORDS = {
    "a", "the", "in", "on", "at", "to", "from", "for", "with", "by", "of", "an", "and", "or", "as", "is"
}

def normalize_token(token: str) -> str:
    token = token.lower()
    for suffix in ['ing', 'ed', 'es', 's']:
        if token.endswith(suffix) and len(token) > len(suffix) + 1:
            token = token[:-len(suffix)]
            break
    return token

def clean_tokens(text: str) -> List[str]:
    tokens = text.replace(",", "").lower().split()
    return [normalize_token(t) for t in tokens if normalize_token(t) not in STOPWORDS]

def match_token_to_slot(
    tokens: List[str],
    slot: str,
    reverse_map: Dict[str, int],
    forward_map: Dict[int, str],
    file_path: str = None
) -> Tuple[int, str]:
    keys = list(reverse_map.keys())

    # Try bigrams first
    bigrams = [" ".join([tokens[i], tokens[i+1]]) for i in range(len(tokens)-1)]
    for phrase in bigrams:
        match = difflib.get_close_matches(phrase, keys, n=1, cutoff=0.85)
        if match:
            return reverse_map[match[0]], match[0]

    # Then fall back to single tokens
    for token in tokens:
        match = difflib.get_close_matches(token, keys, n=1, cutoff=0.85)
        if match:
            return reverse_map[match[0]], match[0]

    # Auto-add (only for certain slots)
    for token in tokens:
        if slot in AUTO_ADD_SLOTS and token not in reverse_map:
            next_code = max(forward_map.keys(), default=0) + 1
            forward_map[next_code] = token
            reverse_map[token] = next_code

            if file_path:
                updated_dict = {f"{k:#06x}": v for k, v in forward_map.items()}
                with open(file_path, "w") as f:
                    json.dump(updated_dict, f, indent=2)

            return next_code, token

    return 0x0000, None


def parse_input_v3(
    text: str,
    reverse_maps: ReverseDict,
    dictionaries: SlotDict,
    file_paths: FilePaths
) -> ResultTuple:
    tokens = clean_tokens(text)
    matched_tokens = set()
    result = {}

    for slot in SLOT_ORDER:
        reverse = reverse_maps.get(slot, {})
        forward = dictionaries.get(slot, {})
        path = file_paths.get(slot)

        code, matched = match_token_to_slot(tokens, slot, reverse, forward, path)

        result[slot] = code

        if matched:
            matched_tokens.add(matched)

    return result