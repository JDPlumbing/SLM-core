def render_clause(clause, suppress_subject=False):
    parts = []

    def safe_add(part):
        if not parts:
            parts.append(part)
            return
        prev_last = parts[-1].split()[-1]
        next_first = part.split()[0]
        if prev_last == next_first:
            part = " ".join(part.split()[1:])
        parts.append(part)

    subj = clause.get("subject")
    verb = clause.get("verb")

    if subj and not suppress_subject:
        if verb and verb.startswith("someone_") and subj != "someone":
            safe_add(subj.replace("_", " "))
            verb = verb[len("someone_"):]
        elif not (verb and subj and verb.startswith(f"{subj}_")):
            safe_add(subj.replace("_", " "))

    if verb:
        verb_phrase = verb.replace("_", " ")
        adverb = clause.get("adverb")
        if adverb:
            verb_phrase += f" {adverb}"
        safe_add(verb_phrase)

    obj = clause.get("object")
    modifier = clause.get("modifier")
    if obj and modifier:
        safe_add(f"{modifier} {obj.replace('_', ' ')}")
    elif obj:
        safe_add(obj.replace("_", " "))

    loc = clause.get("location")
    if loc:
        loc_str = loc.replace("_", " ")
        if loc.startswith(("under_", "beneath_", "below_")):
            preposition = "under"
        elif loc.startswith(("above_", "over_", "overhead_")):
            preposition = "above"
        elif loc.startswith(("behind_",)):
            preposition = "behind"
        elif loc.startswith(("inside_", "within_", "interior_")):
            preposition = "inside"
        elif loc.startswith(("outside_", "beyond_", "exterior_")):
            preposition = "outside"
        else:
            preposition = "in"
        safe_add(f"{preposition} {loc_str}")

    intent = clause.get("intent")
    if intent:
        if intent.startswith("to_"):
            safe_add(f"to {intent[3:]}")
        elif intent.startswith("that_"):
            safe_add(f"so that {intent[5:]}")
        else:
            safe_add(intent)

    cause = clause.get("cause")
    if cause:
        if cause.startswith("to_"):
            safe_add(f"due to {cause[3:]}")
        elif cause.startswith("of_"):
            safe_add(f"because of {cause[3:]}")
        else:
            safe_add(f"from {cause}")

    status = clause.get("status")
    if status:
        safe_add(status.replace("_", " "))

    return " ".join(parts)


def render_clauses(clause_a, clause_b=None):
    sentence = render_clause(clause_a)

    if clause_b:
        subj_a = clause_a.get("subject")
        subj_b = clause_b.get("subject")
        verb_b = clause_b.get("verb")

        suppress_subject = (
            not subj_b or
            subj_b == "someone" or
            subj_b == subj_a or
            (verb_b and subj_b and verb_b.startswith(f"{subj_b}_"))
        )

        rendered_b = render_clause(clause_b, suppress_subject=suppress_subject)
        if rendered_b.strip():
            sentence += ". " + rendered_b

    return sentence.capitalize() + "."
