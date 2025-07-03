import os
import sys
import sqlite3
from wordfreq import top_n_list
import spacy

# POS-compatible SLM slot map
SLOT_POS_MAP = {
    "verb": "VERB",
    "adjective": "ADJ",
    "adverb": "ADV",
    "object": "NOUN",
    "subject": "NOUN",
    "space": "NOUN"
}

# Byte limit assumptions (used for max cap)
SLOT_LIMITS = {
    "verb": 3,
    "object": 3,
    "subject": 2,
    "adjective": 2,
    "adverb": 2,
    "space": 2
}

# Set up spaCy
nlp = spacy.load("en_core_web_sm")

def get_slot_cap(slot):
    bytes_ = SLOT_LIMITS.get(slot, 3)
    return min(2 ** (bytes_ * 8), 5000)

def populate_slot(slot):
    if slot not in SLOT_POS_MAP:
        print(f"⚠️  Skipping '{slot}' (not POS-compatible)")
        return

    pos_tag = SLOT_POS_MAP[slot]
    max_entries = get_slot_cap(slot)

    print(f"\n🔁 Populating '{slot}' with POS {pos_tag}...")

    words = top_n_list("en", 10000)
    filtered = []

    for word in words:
        doc = nlp(word)
        if len(doc) == 1 and doc[0].pos_ == pos_tag:
            filtered.append(word.lower())
        if len(filtered) >= max_entries:
            break

    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "db/slm.sqlite"))
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dictionary WHERE slot = ?", (slot,))
    for word in filtered:
        cursor.execute("INSERT OR IGNORE INTO dictionary (slot, word) VALUES (?, ?)", (slot, word))
    conn.commit()
    conn.close()

    print(f"✅ Imported {len(filtered)} words into slot '{slot}'")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 importer.py [slot|all]")
        print("Available slots:", ", ".join(SLOT_POS_MAP.keys()))
        sys.exit(1)

    target = sys.argv[1].lower()
    if target == "all":
        for slot in SLOT_POS_MAP:
            populate_slot(slot)
    else:
        populate_slot(target)
