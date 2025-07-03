import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
TABLE_NAME = "slm_entries"
DICT_PATH = "dicts"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase config in environment.")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

def sync_dict(slot_id):
    filepath = os.path.join(DICT_PATH, f"{slot_id}.txt")
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        return

    with open(filepath, "r") as f:
        entries = [line.strip() for line in f if line.strip()]

    for entry in entries:
        if "_" in entry:
            word1, word2 = entry.split("_", 1)
        else:
            word1, word2 = entry, None

        payload = {
            "slot_id": slot_id,
            "entry": entry,
            "word1": word1,
            "word2": word2,
        }

        response = requests.post(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}", headers=HEADERS, json=payload)
        if response.status_code == 201:
            print(f"✅ Synced: {entry}")
        elif "duplicate key" in response.text:
            print(f"⏩ Skipped (exists): {entry}")
        else:
            print(f"❌ Error for {entry}: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sync_dict.py <slot_name>")
        sys.exit(1)

    slot_name = sys.argv[1]
    sync_dict(slot_name)
