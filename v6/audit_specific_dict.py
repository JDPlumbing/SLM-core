import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_API_KEY")
TABLE_NAME = "slm_entries"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

def load_local_entries(slot):
    filepath = f"dicts/{slot}.txt"
    if not os.path.exists(filepath):
        print(f"❌ File not found for slot: {slot}")
        return set()

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        lines = [line for line in lines if line and not line.startswith("#")]
        return set(lines)

def fetch_supabase_entries(slot):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?slot_id=eq.{slot}&select=entry"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to fetch from Supabase: {response.status_code} - {response.text}")
        return set()
    return set(item["entry"] for item in response.json())

def audit_slot(slot):
    print(f"\n📦 Slot: {slot}")
    local_entries = load_local_entries(slot)
    supabase_entries = fetch_supabase_entries(slot)

    print(f"   🧮 Local entries: {len(local_entries)}")
    print(f"   🧮 Supabase entries: {len(supabase_entries)}")

    # Show sample local entries
    print("   🔍 Sample entries:")
    for entry in sorted(list(local_entries))[:25]:
        print(f"     - {entry}")

    # Show missing entries
    missing = local_entries - supabase_entries
    if missing:
        print(f"\n   ❌ Missing in Supabase ({len(missing)}):")
        for entry in sorted(missing):
            print(f"     - {entry}")
    else:
        print("   ✅ All local entries exist in Supabase.")

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python audit_specific_dict.py <slot>")
        return

    slot = sys.argv[1].strip()
    audit_slot(slot)

main()
