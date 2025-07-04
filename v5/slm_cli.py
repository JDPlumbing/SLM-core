from slm_tokenizer import tokenize
from slm_renderer import render_clauses  # ✅ Use patched renderer


def pretty_print_clause(label, clause):
    print(f"\n📦 {label}:")
    print("{")
    for k, v in clause.items():
        print(f'  "{k}": {repr(v)},')
    print("}")

    
if __name__ == "__main__":
    print("🧠 SLM CLI v5")
    print("Type a sentence to encode and parse it.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            text = input("🗣️  Say something: ").strip()
            if text.lower() == "exit":
                break

            result = tokenize(text)

            if not isinstance(result, tuple) or len(result) != 2:
                print("❌ Error: tokenize() must return exactly 2 clauses (clause_a, clause_b)")
                continue

            clause_a, clause_b = result

            pretty_print_clause("Clause A", clause_a)
            pretty_print_clause("Clause B", clause_b)

            rendered = render_clauses(clause_a, clause_b)
            print(f"\n🧾 Interpreted:\n{rendered}")
            print("-" * 40)

        except KeyboardInterrupt:
            print("\n👋 Goodbye.")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
