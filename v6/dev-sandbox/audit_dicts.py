import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
TABLE_NAME = "slm_entries"
DICT_PATH = "dicts"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

def load_local_entries():
    local = {}
    for fname in os.listdir(DICT_PATH):
        if fname.endswith(".txt"):
            slot_id = fname.replace(".txt", "")
            with open(os.path.join(DICT_PATH, fname), "r") as f:
                entries = {line.strip().lower() for line in f if line.strip()}
                local[slot_id] = entries
    return local

def load_supabase_entries():
    response = requests.get(f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?select=slot_id,entry", headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    
    supabase = {}
    for row in data:
        slot = row["slot_id"]
        entry = row["entry"].strip().lower()
        supabase.setdefault(slot, set()).add(entry)
    return supabase

def compare(local, remote):
    all_slots = sorted(set(local.keys()) | set(remote.keys()))
    for slot in all_slots:
        local_entries = local.get(slot, set())
        remote_entries = remote.get(slot, set())

        missing = local_entries - remote_entries
        extra = remote_entries - local_entries

        print(f"\n📦 Slot: {slot}")
        print(f"   🧮 Local: {len(local_entries)}  | Supabase: {len(remote_entries)}")

        if missing:
            print(f"   👻 Missing in Supabase ({len(missing)}):")
            for entry in sorted(missing):
                print(f"     - {entry}")
        if extra:
            print(f"   🧟 Extra in Supabase ({len(extra)}):")
            for entry in sorted(extra):
                print(f"     - {entry}")
        if not missing and not extra:
            print(f"   ✅ Perfect match.")

def main():
    local = load_local_entries()
    remote = load_supabase_entries()
    compare(local, remote)

if __name__ == "__main__":
    main()
