import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
TABLE_NAME = "slm_entries"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_API_KEY in environment.")

DICT_PATH = "dicts"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

# These slots allow single-word entries (no underscore required)
ALLOW_SINGLE_WORD = {"adverb", "modifier"}

# Optional: support CLI arg like `--slot verb`
import sys
SLOT_FILTER = None
if len(sys.argv) == 3 and sys.argv[1] == "--slot":
    SLOT_FILTER = sys.argv[2]
    print(f"🔎 Syncing only slot: `{SLOT_FILTER}`\n")

def fetch_existing_entries():
    entries_by_slot = {}
    for slot in os.listdir(DICT_PATH):
        if slot.endswith(".txt"):
            slot_name = slot.replace(".txt", "")
            response = requests.get(
                f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?slot_id=eq.{slot_name}&select=entry",
                headers=HEADERS
            )
            if response.status_code == 200:
                entries = [item["entry"] for item in response.json()]
                entries_by_slot[slot_name] = set(entries)
                print(f"📥 Pulled {len(entries)} existing entries for `{slot_name}`")
            else:
                print(f"❌ Failed to fetch slot `{slot_name}`: {response.text}")
    return entries_by_slot

def upload_missing_entries(entries_by_slot):
    for fname in os.listdir(DICT_PATH):
        if not fname.endswith(".txt"):
            continue
        slot_id = fname.replace(".txt", "")
        if SLOT_FILTER and slot_id != SLOT_FILTER:
            continue

        local_path = os.path.join(DICT_PATH, fname)
        with open(local_path, "r") as f:
            local_entries = set(line.strip() for line in f if line.strip())

        existing = entries_by_slot.get(slot_id, set())
        missing = local_entries - existing

        uploaded, skipped, failed = 0, 0, 0

        for entry in sorted(missing):
            if slot_id not in ALLOW_SINGLE_WORD and "_" not in entry:
                print(f"⚠️ Skipping invalid entry (no underscore): {entry}")
                skipped += 1
                continue

            word1, word2 = (entry.split("_", 1) if "_" in entry else (entry, ""))

            payload = {
                "slot_id": slot_id,
                "entry": entry,
                "word1": word1,
                "word2": word2
            }

            response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}", headers=HEADERS, json=payload)
            if response.status_code == 201:
                print(f"✅ Uploaded: {entry}")
                uploaded += 1
            else:
                print(f"❌ Failed: {entry} | {response.status_code} | {response.text}")
                failed += 1

        print(f"\n📊 Slot `{slot_id}` summary — Uploaded: {uploaded}, Skipped: {skipped}, Failed: {failed}\n")

if __name__ == "__main__":
    data = fetch_existing_entries()
    upload_missing_entries(data)
