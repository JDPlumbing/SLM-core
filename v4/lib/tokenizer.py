import spacy
from db import list_words_by_slot

nlp = spacy.load("en_core_web_sm")

# Load dictionary word sets by slot
SLOT_WORDS = {
    slot: set(word for _, word in list_words_by_slot(slot)) for slot in [
        "verb", "object", "subject", "size", "material", "shape", "color",
        "condition", "purpose", "preposition", "adjective", "adverb",
        "status", "cause", "intent", "space"
    ]
}

def tokenize(text):
    import re
    text = re.sub(r'(\w+)-(\w+)', r'\1_\2', text.lower())  # do lower+replace together
    doc = nlp(text)  # already lowercase, no need to lowercase again
    slots = {}


    # Special case: [VERB] [NOUN] [PREP] [NOUN]
    if len(doc) >= 4:
        for i in range(len(doc) - 3):
            if (doc[i].pos_ == "VERB" and
                doc[i+1].pos_ == "NOUN" and
                doc[i+2].pos_ == "ADP" and
                doc[i+3].pos_ == "NOUN"):

                v, o, p, s = (doc[i].text, doc[i+1].text, doc[i+2].text, doc[i+3].text)
                if v in SLOT_WORDS["verb"]:
                    slots["verb"] = v
                if o in SLOT_WORDS["object"]:
                    slots["object"] = o
                if p in SLOT_WORDS["preposition"]:
                    slots["preposition"] = p
                if s in SLOT_WORDS["space"]:
                    slots["space"] = s
                break

    # General POS-aware fallback
    for token in doc:
        word = token.text.strip().lower()
        if word in slots.values():
            continue  # Already assigned to a slot

        if token.pos_ == "PRON" and "subject" not in slots and word in SLOT_WORDS["subject"]:
            slots["subject"] = word
        elif token.pos_ == "NOUN":
            prev = doc[token.i - 1].text.lower() if token.i > 0 else ""
            is_obj = word in SLOT_WORDS["object"]
            is_space = word in SLOT_WORDS["space"]

            if is_space and prev in ("in", "on", "under") and "space" not in slots:
                slots["space"] = word
            elif is_obj and prev in ("a", "an", "the") and "object" not in slots:
                slots["object"] = word
            elif is_obj and "object" not in slots and not is_space:
                slots["object"] = word
            elif is_space and "space" not in slots:
                slots["space"] = word
        elif token.pos_ == "VERB" and "verb" not in slots and word in SLOT_WORDS["verb"]:
            slots["verb"] = word
        elif token.pos_ == "ADJ" and "adjective" not in slots and word in SLOT_WORDS["adjective"]:
            slots["adjective"] = word
        elif token.pos_ == "ADV" and "adverb" not in slots and word in SLOT_WORDS["adverb"]:
            slots["adverb"] = word
        elif token.pos_ == "ADP" and "preposition" not in slots and word in SLOT_WORDS["preposition"]:
            slots["preposition"] = word
        else:
            # Fuzzy fallback pass
            for slot, word_set in SLOT_WORDS.items():
                if slot not in slots and word in word_set:
                    slots[slot] = word
                    break

    return slots
