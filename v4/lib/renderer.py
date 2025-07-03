def render(slot_dict):
    parts = []

    # Subject + Verb
    if slot_dict.get("subject"):
        parts.append(slot_dict["subject"])
    if slot_dict.get("verb"):
        parts.append(slot_dict["verb"])

    # Pre-object modifiers
    for mod in ["adjective", "color", "condition", "size", "material", "shape"]:
        val = slot_dict.get(mod)
        if val:
            parts.append(val)

    # Object
    if slot_dict.get("object"):
        parts.append(slot_dict["object"])

    # Prepositional phrase (e.g. "in the bathroom")
    prep = slot_dict.get("preposition")
    space = slot_dict.get("space")
    if prep and space:
        parts.append(f"{prep} the {space}")
    elif space:
        parts.append(f"in the {space}")

    # Adverb
    if slot_dict.get("adverb"):
        parts.append(slot_dict["adverb"])

    # Cause, Intent, Status (trailing tags)
    extras = []
    if slot_dict.get("cause"):
        extras.append(f"due to {slot_dict['cause']}")
    if slot_dict.get("intent"):
        extras.append(f"to {slot_dict['intent']}")
    if slot_dict.get("status"):
        extras.append(f"({slot_dict['status']})")

    if extras:
        parts.append(" ".join(extras))

    if not parts:
        return "[No valid slots to render]"

    return " ".join(parts).capitalize() + "."

# Test CLI
if __name__ == "__main__":
    sample = {
        "subject": "plumber",
        "verb": "installed",
        "color": "red",
        "object": "toilet",
        "space": "bathroom",
        "cause": "leak"
    }
    print(render(sample))