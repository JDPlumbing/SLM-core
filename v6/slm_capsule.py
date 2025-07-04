from typing import Dict

SLOT_ORDER = [
    "subject", "verb", "object", "location",
    "intent", "cause", "status", "adverb"
]

CLAUSE_SIZE = 16  # bytes per clause
HEADER_SIZE = 2   # version, masks, context
FOOTER_SIZE = 2   # checksum or chainref
CAPSULE_SIZE = HEADER_SIZE + CLAUSE_SIZE * 2 + FOOTER_SIZE


def encode_clause(clause: Dict[str, str], slot_indices: Dict[str, int]) -> bytes:
    b = bytearray()
    for slot in SLOT_ORDER:
        val = clause.get(slot)
        index = slot_indices.get(val, 0) if val else 0
        b += index.to_bytes(2, byteorder="big")
    return bytes(b)


def decode_clause(data: bytes, slot_lookup: Dict[str, Dict[int, str]]) -> Dict[str, str]:
    clause = {}
    for i, slot in enumerate(SLOT_ORDER):
        raw = int.from_bytes(data[i * 2:i * 2 + 2], byteorder="big")
        value = slot_lookup.get(slot, {}).get(raw, None)
        clause[slot] = value
    return clause


def encode(slots: Dict[str, Dict[str, str]], slot_indices: Dict[str, int]) -> bytes:
    header = (0).to_bytes(2, byteorder="big")  # placeholder
    clause_a = encode_clause(slots.get("clause_a", {}), slot_indices)
    clause_b = encode_clause(slots.get("clause_b", {}), slot_indices)
    footer = (0).to_bytes(2, byteorder="big")  # placeholder
    return header + clause_a + clause_b + footer


def decode(capsule: bytes, slot_lookup: Dict[str, Dict[int, str]]) -> Dict[str, Dict[str, str]]:
    if len(capsule) != CAPSULE_SIZE:
        raise ValueError("Capsule must be 36 bytes")
    clause_a = decode_clause(capsule[2:18], slot_lookup)
    clause_b = decode_clause(capsule[18:34], slot_lookup)
    return {"clause_a": clause_a, "clause_b": clause_b}
