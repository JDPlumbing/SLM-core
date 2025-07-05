# slm_capsule.py (v7)
from typing import Dict

SLOT_ORDER = [
    "subject", "verb", "object", "location",
    "intent", "cause", "status", "adverb"
]

CLAUSE_SIZE = 16  # bytes per clause
HEADER_SIZE = 2
FOOTER_SIZE = 2
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

def clause_mask(clause: dict) -> int:
    return sum(1 << i for i, slot in enumerate(SLOT_ORDER) if clause.get(slot) is not None)

def build_header(version: int, clause_a: dict, clause_b: dict, context: int = 0) -> bytes:
    if not (0 <= version < 2**4):
        raise ValueError("version must be 0–15 (4 bits)")
    if not (0 <= context < 2**4):
        raise ValueError("context must be 0–15 (4 bits)")
    mask_a = clause_mask(clause_a) & 0xF
    mask_b = clause_mask(clause_b) & 0xF
    val = (version << 12) | (mask_a << 8) | (mask_b << 4) | context
    return val.to_bytes(2, "big")

def build_footer(event_ref: int, flags: int = 0) -> bytes:
    if not (0 <= event_ref < 2**12):
        raise ValueError("event_ref must be 0–4095 (12 bits)")
    if not (0 <= flags < 2**4):
        raise ValueError("flags must be 0–15 (4 bits)")
    val = (event_ref << 4) | flags
    return val.to_bytes(2, "big")

def parse_header(header: bytes) -> tuple[int, int, int, int]:
    val = int.from_bytes(header, "big")
    return (val >> 12) & 0xF, (val >> 8) & 0xF, (val >> 4) & 0xF, val & 0xF

def parse_footer(footer: bytes) -> tuple[int, int]:
    val = int.from_bytes(footer, "big")
    return (val >> 4) & 0xFFF, val & 0xF

def encode(slots: Dict[str, Dict[str, str]], slot_indices: Dict[str, int], version: int = 1, context: int = 0, event_ref: int = 0, flags: int = 0) -> bytes:
    clause_a = encode_clause(slots.get("clause_a", {}), slot_indices)
    clause_b = encode_clause(slots.get("clause_b", {}), slot_indices)
    header = build_header(version, slots.get("clause_a", {}), slots.get("clause_b", {}), context)
    footer = build_footer(event_ref, flags)
    return header + clause_a + clause_b + footer

def decode(capsule: bytes, slot_lookup: Dict[str, Dict[int, str]]) -> Dict[str, Dict[str, str]]:
    if len(capsule) != CAPSULE_SIZE:
        raise ValueError("Capsule must be 36 bytes")
    clause_a = decode_clause(capsule[2:18], slot_lookup)
    clause_b = decode_clause(capsule[18:34], slot_lookup)
    return {"clause_a": clause_a, "clause_b": clause_b}