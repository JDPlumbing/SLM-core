from lib.translator_v2 import (
    load_all_dictionaries,
    normalize_slots,
    render_structured
)
from lib.translator_v3 import parse_input_v3

from lib.renderer_english import render_english

def main():
    dictionaries, reverse_maps, file_paths = load_all_dictionaries("diction")  # ✅ Unpack all 3

    print("SLM Pipeline CLI: Type your input (or 'exit')")

    while True:
        raw = input("> ").strip()
        if raw.lower() in ("exit", "quit"):
            break

        # ✅ Pass all required arguments to parse_input
        parsed = parse_input_v3(raw, reverse_maps, dictionaries, file_paths)

        normalized = normalize_slots(parsed)

        print("\n[Normalized Tuple]:")
        for k in sorted(normalized):
            print(f"  {k}: {hex(normalized[k]) if normalized[k] else '0x0000'}")

        print("\n[Rendered English]:")
        print(render_english(normalized, dictionaries))

        print("\n[Structured Full Output]:")
        print(render_structured(normalized, dictionaries))

        print("-" * 40)

if __name__ == "__main__":
    main()
