# slm_parser.py

SLOT_ORDER = [
    "subject", "verb", "object", "modifier",
    "location", "intent", "cause", "status", "adverb"
]

def parse_tokens(tokens):
    clause_a = {slot: None for slot in SLOT_ORDER}
    clause_b = {slot: None for slot in SLOT_ORDER}

    current_clause = clause_a

    for slot, value in tokens:
        if slot == "unknown":
            continue
        if current_clause[slot] is None:
            current_clause[slot] = value
        elif clause_b[slot] is None:
            current_clause = clause_b
            clause_b[slot] = value
        # If both A and B have the slot filled, skip (could log this)

    return clause_a, clause_b

# Optional CLI test
if __name__ == "__main__":
    test_tokens = [
        ("subject", "he_will"),
        ("verb", "will_fix"),
        ("object", "the_pipe"),
        ("modifier", "leaking"),
        ("cause", "to_corrosion"),
        ("subject", "i_will"),
        ("verb", "will_replace")
    ]
    a, b = parse_tokens(test_tokens)
    print("Clause A:", a)
    print("Clause B:", b)