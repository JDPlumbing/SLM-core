import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "lib")))

from db import (
    add_word,
    get_id,
    get_word,
    list_words_by_slot,
    connect_db,
    initialize_db
)

try:
    from spellchecker import SpellChecker
    spell = SpellChecker()
except ImportError:
    spell = None

print("\n📘 SLM Dictionary CLI")
print("Commands: add [slot] [word], list [slot], get [slot] [word/id], get-all [slot], delete [slot] [word/id], stats, export [slot], audit [slot], search [text], edit [slot] [old_word] [new_word], spellcheck [slot], fix [slot] [wrong_word] [correct_word], q")

initialize_db()

while True:
    raw = input("dict> ").strip()
    if raw.lower() in ("q", "quit", "exit"):
        break

    parts = raw.split()
    if not parts:
        continue

    cmd = parts[0].lower()

    if cmd == "add" and len(parts) >= 3:
        slot = parts[1].lower()
        word = " ".join(parts[2:]).lower()
        add_word(slot, word)

    elif cmd == "list" and len(parts) == 2:
        slot = parts[1].lower()
        words = list_words_by_slot(slot)
        if not words:
            print("(empty)")
        else:
            for wid, word in words:
                print(f"{wid:04d}  {word}")

    elif cmd == "get-all" and len(parts) == 2:
        slot = parts[1].lower()
        words = list_words_by_slot(slot)
        if not words:
            print("(empty)")
        else:
            for wid, word in words:
                print(f"{wid:04d}  {word}")

    elif cmd == "get" and len(parts) == 3:
        slot = parts[1].lower()
        key = parts[2].lower()
        if key.isdigit():
            word = get_word(slot, int(key))
            print(f"id {key} → {word}" if word else "Not found")
        else:
            wid = get_id(slot, key)
            print(f"{key} → id {wid}" if wid else "Not found")

    elif cmd == "delete" and len(parts) == 3:
        slot = parts[1].lower()
        key = parts[2].lower()
        conn = connect_db()
        cursor = conn.cursor()
        if key.isdigit():
            cursor.execute("DELETE FROM dictionary WHERE slot = ? AND id = ?", (slot, int(key)))
        else:
            cursor.execute("DELETE FROM dictionary WHERE slot = ? AND word = ?", (slot, key))
        conn.commit()
        conn.close()
        print("✅ Deleted if existed")

    elif cmd == "stats":
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT slot, COUNT(*) FROM dictionary GROUP BY slot ORDER BY slot")
        for slot, count in cursor.fetchall():
            print(f"{slot:12s} {count:4d} entries")
        conn.close()

    elif cmd == "export" and len(parts) == 2:
        slot = parts[1].lower()
        words = list_words_by_slot(slot)
        export_path = f"{slot}_export.json"
        with open(export_path, "w") as f:
            json.dump({str(wid): word for wid, word in words}, f, indent=2)
        print(f"✅ Exported to {export_path}")

    elif cmd == "audit" and len(parts) == 2:
        slot = parts[1].lower()
        words = list_words_by_slot(slot)
        ids = [wid for wid, _ in words]
        print(f"🔍 Total entries: {len(ids)}")
        if not ids:
            print("(empty)")
        elif ids != list(sorted(ids)):
            print("⚠️  Non-sequential IDs detected")
        if len(set(ids)) != len(ids):
            print("⚠️  Duplicate IDs detected")
        seen = set()
        for _, word in words:
            if word in seen:
                print(f"⚠️  Duplicate word: {word}")
            seen.add(word)
        print("✅ Audit complete")

    elif cmd == "search" and len(parts) >= 2:
        term = " ".join(parts[1:]).lower()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT slot, id, word FROM dictionary WHERE word LIKE ?", (f"%{term}%",))
        results = cursor.fetchall()
        for slot, wid, word in results:
            print(f"{slot:10s} {wid:04d}  {word}")
        conn.close()

    elif cmd == "edit" and len(parts) >= 4:
        slot = parts[1].lower()
        old = parts[2].strip().lower()
        new = " ".join(parts[3:]).strip().lower()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE dictionary SET word = ? WHERE slot = ? AND word = ?", (new, slot, old))
        if cursor.rowcount:
            print(f"✅ Updated '{old}' → '{new}'")
        else:
            print("⚠️  Word not found or unchanged")
        conn.commit()
        conn.close()

    elif cmd == "spellcheck" and len(parts) == 2:
        if not spell:
            print("❌ Spellchecker module not available. Run: pip install pyspellchecker")
            continue
        slot = parts[1].lower()
        words = [word for _, word in list_words_by_slot(slot)]
        misspelled = spell.unknown(words)
        if not misspelled:
            print("✅ No potential spelling issues found.")
        else:
            for word in sorted(misspelled):
                suggestions = spell.candidates(word)
                if suggestions:
                    print(f"⚠️  Possibly incorrect: {word} → suggestions: {', '.join(suggestions)}")
                else:
                    print(f"⚠️  Possibly incorrect: {word} → no suggestions")

    elif cmd == "fix" and len(parts) >= 4:
        slot = parts[1].lower()
        wrong = parts[2].strip().lower()
        corrected = " ".join(parts[3:]).strip().lower()
        conn = connect_db()
        cursor = conn.cursor()
        # Check if corrected already exists
        cursor.execute("SELECT id FROM dictionary WHERE slot = ? AND word = ?", (slot, corrected))
        if cursor.fetchone():
            cursor.execute("DELETE FROM dictionary WHERE slot = ? AND word = ?", (slot, wrong))
            conn.commit()
            print(f"✅ Removed '{wrong}' (already present as '{corrected}')")
        else:
            cursor.execute("UPDATE dictionary SET word = ? WHERE slot = ? AND word = ?", (corrected, slot, wrong))
            if cursor.rowcount:
                print(f"✅ Fixed '{wrong}' → '{corrected}'")
            else:
                print("⚠️  Word not found or unchanged")
            conn.commit()
        conn.close()

    elif cmd == "auto-fix" and len(parts) == 2:
        if not spell:
            print("❌ Spellchecker module not available. Run: pip install pyspellchecker")
            continue
        slot = parts[1].lower()
        words = list_words_by_slot(slot)
        misspelled = spell.unknown([w for _, w in words])
        if not misspelled:
            print("✅ No spelling issues detected.")
            continue

        conn = connect_db()
        cursor = conn.cursor()
        for wid, word in words:
            if word not in misspelled:
                continue
            candidates = spell.candidates(word)
            if candidates is None:
                candidates = set()

            if len(candidates) == 1:
                corrected = list(candidates)[0]
                cursor.execute("SELECT id FROM dictionary WHERE slot = ? AND word = ?", (slot, corrected))
                if cursor.fetchone():
                    cursor.execute("DELETE FROM dictionary WHERE slot = ? AND word = ?", (slot, word))
                    print(f"✅ Removed '{word}' (already exists as '{corrected}')")
                else:
                    cursor.execute("UPDATE dictionary SET word = ? WHERE slot = ? AND word = ?", (corrected, slot, word))
                    print(f"✅ Fixed '{word}' → '{corrected}'")
            elif len(candidates) == 0:
                cursor.execute("DELETE FROM dictionary WHERE slot = ? AND word = ?", (slot, word))
                print(f"❌ Deleted '{word}' (no suggestions)")
            else:
                print(f"⚠️ Skipped '{word}' → multiple suggestions")

        conn.commit()
        conn.close()

    elif cmd == "find-pattern" and len(parts) == 2:
        pattern = parts[1].lower()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT slot, id, word FROM dictionary WHERE word LIKE ?", (f"%{pattern}%",))
        results = cursor.fetchall()
        if not results:
            print("✅ No matches found.")
        else:
            for slot, wid, word in results:
                print(f"{slot:10s} {wid:04d}  {word}")
        conn.close()
    
    elif cmd == "fix-suffix" and len(parts) == 4:
        slot = parts[1].lower()
        from_suffix = parts[2].lower()
        to_suffix = parts[3].lower()
        words = list_words_by_slot(slot)

        conn = connect_db()
        cursor = conn.cursor()

        for wid, word in words:
            if word.endswith(from_suffix):
                corrected = word[:-len(from_suffix)] + to_suffix
                cursor.execute("SELECT id FROM dictionary WHERE slot = ? AND word = ?", (slot, corrected))
                if cursor.fetchone():
                    cursor.execute("DELETE FROM dictionary WHERE slot = ? AND word = ?", (slot, word))
                    print(f"✅ Removed '{word}' (already exists as '{corrected}')")
                else:
                    cursor.execute("UPDATE dictionary SET word = ? WHERE slot = ? AND word = ?", (corrected, slot, word))
                    print(f"✅ Fixed '{word}' → '{corrected}'")
        conn.commit()
        conn.close()

    else:
        print("Unknown command or invalid syntax")
