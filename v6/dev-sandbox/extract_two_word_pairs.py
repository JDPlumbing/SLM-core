import re

INPUT_FILE = "glossary.txt"
OUTPUT_FILE = "glossary_chunks.txt"

def clean_word(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())

def extract_pairs(words):
    pairs = set()
    for offset in [0, 1]:
        for i in range(offset, len(words) - 1):
            w1 = clean_word(words[i])
            w2 = clean_word(words[i+1])
            if w1 and w2:
                pairs.add(f"{w1}_{w2}")
    return pairs

def main():
    with open(INPUT_FILE, "r") as f:
        text = f.read()

    words = text.split()
    all_pairs = extract_pairs(words)

    with open(OUTPUT_FILE, "w") as out:
        for pair in sorted(all_pairs):
            out.write(pair + "\n")

    print(f"✅ Extracted {len(all_pairs)} unique 2-word chunks to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
