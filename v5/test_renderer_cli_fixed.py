import json
from slm_renderer import render_clauses

def main():
    print("🔍 SLM Renderer")
    print("Enter JSON dicts for Clause A and optionally Clause B.")
    print("Leave Clause B empty to skip.\n")

    try:
        clause_a = input("Clause A JSON: ").strip()
        clause_b = input("Clause B JSON (optional): ").strip()

        clause_a_dict = json.loads(clause_a)
        clause_b_dict = json.loads(clause_b) if clause_b else None

        result = render_clauses(clause_a_dict, clause_b_dict)
        print("\n🧠 Rendered Sentence:")
        print(result)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()