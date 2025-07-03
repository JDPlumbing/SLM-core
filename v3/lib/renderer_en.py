def render_english(slot_dict):
    parts = []

    # Subject → Verb
    subject = slot_dict.get("subject")
    if subject and not subject.startswith("<"):
        parts.append(subject)

    verb = slot_dict.get("verb")
    if verb and not verb.startswith("<"):
        parts.append(verb)

    # Modifiers before object
    for modifier in ["adjective", "color", "condition", "size", "material", "shape"]:
        val = slot_dict.get(modifier)
        if val and not val.startswith("<"):
            parts.append(val)

    # Object
    obj = slot_dict.get("object")
    if obj and not obj.startswith("<"):
        parts.append(obj)

    # Preposition + Space
    preposition = slot_dict.get("preposition")
    space = slot_dict.get("space")
    if preposition and not preposition.startswith("<"):
        phrase = preposition
        if space and not space.startswith("<"):
            phrase += f" the {space}"
        parts.append(phrase)
    elif space and not space.startswith("<"):
        parts.append(f"in the {space}")

    # Trailing tags (optional)
    adverb = slot_dict.get("adverb")
    if adverb and not adverb.startswith("<"):
        parts.append(adverb)

    # Optional causal/info tags
    tail_parts = []

    cause = slot_dict.get("cause")
    if cause and not cause.startswith("<"):
        tail_parts.append(f"due to {cause}")

    intent = slot_dict.get("intent")
    if intent and not intent.startswith("<"):
        tail_parts.append(f"to {intent}")

    status = slot_dict.get("status")
    if status and not status.startswith("<"):
        tail_parts.append(f"({status})")

    if tail_parts:
        parts.append(" ".join(tail_parts))

    if not parts:
        return "[No valid slots to render]"

    return " ".join(parts).capitalize() + "."
