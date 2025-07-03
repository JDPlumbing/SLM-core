def render_clause(clause):
    parts = []

    subj = clause.get("subject")
    if subj:
        parts.append(subj.split("_")[0])

    verb = clause.get("verb")
    if verb:
        parts.append(verb.replace("_", " "))

    adverb = clause.get("adverb")
    if adverb:
        parts.append(adverb)

    obj = clause.get("object")
    if obj:
        modifier = clause.get("modifier")
        if modifier:
            parts.append(f"{modifier} {obj.replace('_', ' ')}")
        else:
            parts.append(obj.replace("_", " "))

    loc = clause.get("location")
    if loc:
        parts.append(f"in {loc.replace('_', ' ')}")

    intent = clause.get("intent")
    if intent:
        if intent.startswith("to_"):
            parts.append(f"to {intent[3:]}")
        elif intent.startswith("that_"):
            parts.append(f"so that {intent[5:]}")
        else:
            parts.append(intent)

    cause = clause.get("cause")
    if cause:
        if cause.startswith("to_"):
            parts.append(f"due to {cause[3:]}")
        elif cause.startswith("of_"):
            parts.append(f"because of {cause[3:]}")
        else:
            parts.append(f"from {cause}")

    status = clause.get("status")
    if status:
        parts.append(status.replace("_", " "))

    return " ".join(parts)

def render_clauses(clause_a, clause_b=None):
    sentence = render_clause(clause_a)
    if clause_b:
        rendered_b = render_clause(clause_b)
        if rendered_b.strip():
            sentence += ". " + rendered_b
    return sentence.capitalize() + "."