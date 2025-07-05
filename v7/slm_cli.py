# slm_cli.py — uses updated greedy tokenizer
from slm_tokenizer import tokenize, load_dictionaries

print("🧠 SLM CLI v7")
print("Type a sentence to encode and parse it.")
print("Type 'exit' to quit.\n")

dicts = load_dictionaries()

while True:
    try:
        sent = input("🗣️  Say something: ").strip()
        if sent.lower() in ["exit", "quit"]:
            break

        a, b = tokenize(sent, dicts)
        print("\n📦 Clause A:")
        print(a)
        print("\n📦 Clause B:")
        print(b)
        print("\n🧾 Raw Match:")
        print(" ".join([v for v in a.values() if v] + [v for v in b.values() if v]))
        print("-" * 40)

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        break
