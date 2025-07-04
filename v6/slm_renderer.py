SLOT_ORDER = [
    "subject", "verb", "object", "location",
    "intent", "cause", "status", "adverb"
]

def render_clause_v6(clause):
    parts = []

    def safe_add(part):
        if not part:
            return
        if not parts:
            parts.append(part)
            return
        prev_last = parts[-1].split()[-1]
        curr_words = part.split()
        if curr_words[0] == prev_last:
            curr_words = curr_words[1:]
        if curr_words:
            parts.append(" ".join(curr_words))

    for slot in SLOT_ORDER:
        val = clause.get(slot)
        if val:
            safe_add(val.replace("_", " "))

    return " ".join(parts)

def render_clauses_v6(clause_a, clause_b=None):
    a_str = render_clause_v6(clause_a)
    b_str = render_clause_v6(clause_b) if clause_b and any(clause_b.values()) else ""
    full = a_str
    if b_str:
        full += ". " + b_str
    return full.strip().capitalize() + "."
