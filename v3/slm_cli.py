import json
import sys
import os

# Add ./lib to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "lib")))

from slm_tokenizer import match_slots as tokenize_to_slots
from encoder import encode_slot_dict as encode_slots
from decoder import decode_bytecode
from dictionaries import load_dictionaries
from renderer_en import render_english
from slm_normalizer import normalize_tokens  # ✅ CORRECT IMPORT

dict_map = load_dictionaries()
# Build a flat list of all valid words from the loaded dicts
valid_words = set()
for slot in dict_map.values():
    valid_words.update(slot["rev"].keys())


print("\n🧠 SLM v3 — Full Pipeline Playground")
print("Type a natural input (e.g. 'installed red toilet')")
print("Or type 'q' to quit.\n")

while True:
    raw = input(">>> ").strip()
    if raw.lower() == "q":
        break

    print("\n🧠 Tokenizing...")
    tokens = normalize_tokens(raw, valid_words)  # ✅ Normalizing BEFORE tokenization
    slots = tokenize_to_slots(" ".join(tokens))  # ✅ Match after cleaning
    print(json.dumps(slots, indent=2))

    if not slots.get("verb"):
        print("❌ No verb found. Skipping encoding.\n")
        continue

    try:
        print("\n🔐 Encoding...")
        bytecode = encode_slots(slots, dict_map)
        print(f"🧬 Bytecode: {bytecode.hex()}")
    except Exception as e:
        print(f"❌ Encoding error: {e}")
        continue

    print("\n🔓 Decoding...")
    decoded = decode_bytecode(bytecode, dict_map)
    print(json.dumps(decoded, indent=2))

    print("\n🗣️ Rendering...")
    print(render_english(decoded))
