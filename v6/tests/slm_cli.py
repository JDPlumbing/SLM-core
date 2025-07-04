import json
from slm_tokenizer import tokenize
from slm_parser import parse_tokens
from slm_renderer import render_clauses

def main():
    print("🧠 SLM CLI v5")
    print("Type a sentence to encode and parse it.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("🗣️  Say something: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        try:
            tokens = tokenize(user_input)
            clause_a, clause_b = parse_tokens(tokens)
            print("\n📦 Clause A:")
            print(json.dumps(clause_a, indent=2))
            if clause_b and any(clause_b.values()):
                print("\n📦 Clause B:")
                print(json.dumps(clause_b, indent=2))
            print("\n🧾 Interpreted:")
            print(render_clauses(clause_a, clause_b))
            print("-" * 40)

        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()