import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "lib")))

from tokenizer import tokenize
from renderer import render


print("\n🧠 SLM v4 — Natural Language Structurer")
print("Type a natural phrase (e.g. 'installed red toilet in bathroom')")
print("Or type 'q' to quit.\n")

while True:
    raw = input(">>> ").strip()
    if raw.lower() in ("q", "quit", "exit"):
        break

    print("\n🧠 Tokenizing...")
    slots = tokenize(raw)
    print("Slots:", slots)

    print("\n🗣️ Rendering...")
    print(render(slots))
    print("\n---\n")