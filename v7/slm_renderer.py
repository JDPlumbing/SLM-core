# slm_renderer.py — slot prefix-aware dumb renderer

# slot prefix → readable words
SLOT_PREFIXES = {
    "!": "someone",
    "!!": "someone",
    "#": "the",
    "##": "some",
    "@": "in",
    "@@": "somewhere in",
    "~": "",
    "~~": "",
    ">": "to",
    ">>": "for",
    "<": "because of",
    "<<": "due to",
    ":": "was",
    "::": "is",
    "-": "",
    "--": ""
}

def render(slots):
    parts = []
    for key in ["subject", "verb", "object", "location", "intent", "cause", "status", "adverb"]:
        val = slots.get(key)
        if val:
            prefix = val[:2] if val[:2] in SLOT_PREFIXES else val[:1]
            content = val[2:] if prefix in ["!!", "##", "@@", "~~", ">>", "<<", "::", "--"] else val[1:]
            phrase = SLOT_PREFIXES.get(prefix, "")
            if phrase:
                parts.append(f"{phrase} {content.replace('_', ' ')}")
            else:
                parts.append(content.replace('_', ' '))
    return " ".join(parts)

# For debugging
if __name__ == "__main__":
    example = {
        "subject": "!someone_we",
        "verb": "~has_installed",
        "object": "#leaky_plate",
        "location": "@_bathroom",
        "intent": ">to_fix",
        "cause": "<<_leak",
        "status": None,
        "adverb": None,
    }
    print(render(example))
