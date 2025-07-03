import sqlite3
import os
import json

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/slm.sqlite"))

# Byte limits per slot
SLOT_BUDGET = {
    "verb": 3,
    "object": 3,
    "subject": 2,
    "size": 2,
    "material": 2,
    "shape": 2,
    "color": 1,
    "condition": 1,
    "purpose": 2,
    "preposition": 1,
    "adjective": 2,
    "adverb": 2,
    "status": 1,
    "cause": 3,
    "intent": 3,
    "space": 2
}

# Connect
def connect_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

# Initialize DB
def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dictionary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot TEXT NOT NULL,
            word TEXT NOT NULL,
            UNIQUE(slot, word)
        )
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_slot_word ON dictionary(slot, word)
    """)
    conn.commit()
    conn.close()

# Add word with slot byte limit check
def add_word(slot, word):
    word = word.strip().lower()
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM dictionary WHERE slot = ?", (slot,))
    count = cursor.fetchone()[0]
    byte_limit = SLOT_BUDGET.get(slot, 3)
    max_entries = 2 ** (byte_limit * 8)
    if count >= max_entries:
        print(f"❌ Cannot add '{word}': slot '{slot}' exceeds {max_entries} entries ({byte_limit} bytes)")
        conn.close()
        return

    cursor.execute(
        "INSERT OR IGNORE INTO dictionary (slot, word) VALUES (?, ?)",
        (slot, word)
    )
    conn.commit()
    conn.close()
    print(f"✅ Added '{word}' to slot '{slot}'")

# Get ID for word in a given slot
def get_id(slot, word):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM dictionary WHERE slot = ? AND word = ?", (slot, word.strip().lower()))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# Get word by ID and slot
def get_word(slot, id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM dictionary WHERE slot = ? AND id = ?", (slot, id))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# List all words by slot
def list_words_by_slot(slot):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, word FROM dictionary WHERE slot = ? ORDER BY word", (slot,))
    words = cursor.fetchall()
    conn.close()
    return words

# Import from legacy v3 dict JSON files
DICT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../v3/dict"))
DICT_SLOT_MAP = {
    "verbs": "verb", "objects": "object", "subjects": "subject", "sizes": "size",
    "materials": "material", "shapes": "shape", "colors": "color", "conditions": "condition",
    "purposes": "purpose", "prepositions": "preposition", "adjectives": "adjective",
    "adverbs": "adverb", "statuses": "status", "causes": "cause", "spaces": "space", "intents": "intent"
}

def import_from_json():
    conn = connect_db()
    cursor = conn.cursor()
    for fname in os.listdir(DICT_DIR):
        if fname.endswith(".json"):
            slot = DICT_SLOT_MAP.get(fname[:-5])
            if not slot:
                continue
            with open(os.path.join(DICT_DIR, fname), 'r') as f:
                data = json.load(f)
            for _, word in data.items():
                word = word.strip().lower()
                cursor.execute("SELECT COUNT(*) FROM dictionary WHERE slot = ?", (slot,))
                count = cursor.fetchone()[0]
                byte_limit = SLOT_BUDGET.get(slot, 3)
                max_entries = 2 ** (byte_limit * 8)
                if count >= max_entries:
                    print(f"❌ Skipped '{word}': slot '{slot}' at capacity")
                    continue
                cursor.execute("INSERT OR IGNORE INTO dictionary (slot, word) VALUES (?, ?)", (slot, word))
    conn.commit()
    conn.close()
    print("✅ Imported legacy dicts.")

if __name__ == "__main__":
    initialize_db()
    import_from_json()
