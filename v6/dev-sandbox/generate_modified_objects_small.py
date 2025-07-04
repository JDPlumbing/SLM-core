import os

DICT_PATH = "dicts"
NOUN_FILE = "object-noun.txt"
MOD_FILE = "object-modifier.txt"
OUTPUT_FILE = "modified_objects_sm.txt"

def load_words(filename):
    path = os.path.join(DICT_PATH, filename)
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return []
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def write_combos(modifiers, nouns, output_path):
    total = 0
    with open(output_path, "w") as f:
        for mod in modifiers:
            for noun in nouns:
                combo = f"{mod}_{noun}"
                f.write(combo + "\n")
                total += 1
    print(f"✅ Wrote {total} entries to {OUTPUT_FILE}")

def main():
    print("🔍 Reading modifier and noun lists...")
    modifiers = load_words(MOD_FILE)
    nouns = load_words(NOUN_FILE)

    if not modifiers:
        print("❌ No modifiers loaded.")
        return
    if not nouns:
        print("❌ No nouns loaded.")
        return

    print(f"✅ Loaded {len(modifiers)} modifiers and {len(nouns)} nouns.")
    output_path = os.path.join(DICT_PATH, OUTPUT_FILE)
    write_combos(modifiers, nouns, output_path)

if __name__ == "__main__":
    main()
