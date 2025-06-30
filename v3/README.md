
# 🧠 SLM-core v3.0.0

**Structured Language Model (SLM)** — a compact, slot-based encoder for translating fuzzy human input into machine-readable bytecode.

Built for field logs, trust protocols, and structured AI inference.

---

## 🚀 What It Does

SLM v3 takes messy, natural language like:

```
"Installed red toilet upstairs due to leak"
```

...and turns it into a tightly packed 32-byte hexcode:

```
000a060000c20000000000000000510000000000000000000000000000002d
```

That hexcode maps to 16 structured slots like:

```json
{
  "verb": "installed",
  "object": "toilet",
  "color": "red",
  "adverb": "upstairs",
  "cause": "leak"
}
```

...and renders clean output like:

```
Installed red toilet upstairs due to leak.
```

---

## 📦 Project Layout

```
SLM-core/
├── v3/
│   ├── lib/
│   │   ├── encoder.py          # Slot → bytecode
│   │   ├── decoder.py          # Bytecode → slot
│   │   ├── renderer_en.py      # Slot → natural English
│   │   ├── slm_tokenizer.py    # Token → slot (via dictionaries)
│   │   ├── slm_normalizer.py   # Fuzzy spell-correction + preprocessing
│   │   └── dictionaries.py     # Loads all dicts into usable maps
│   ├── dict/
│   │   ├── verbs.json
│   │   ├── objects.json
│   │   ├── (etc... 16 total)
│   ├── slm_cli.py              # Playground CLI
│   └── README.md
```

---

## 🧩 16 Semantic Slots

Each natural-language statement is parsed into **16 slots**, each with a fixed byte-width.

| Slot Name    | Bytes | Example           |
|--------------|-------|-------------------|
| `verb`       | 3     | install           |
| `object`     | 3     | toilet            |
| `subject`    | 2     | plumber           |
| `size`       | 2     | 1in               |
| `material`   | 2     | copper            |
| `shape`      | 2     | round             |
| `color`      | 1     | red               |
| `condition`  | 1     | new               |
| `purpose`    | 2     | upgrade           |
| `preposition`| 1     | under             |
| `adjective`  | 2     | broken            |
| `adverb`     | 2     | upstairs          |
| `status`     | 1     | complete          |
| `cause`      | 3     | leak              |
| `intent`     | 3     | replace           |
| `space`      | 2     | bathroom          |

---

## 🧪 Try It Locally

Run the CLI:

```bash
cd SLM-core/v3
python3 slm_cli.py
```

Then enter fuzzy phrases like:

```
>>> installd copperr toileet bathroom
```

SLM will:
1. Normalize spelling (`installed`, `copper`, `toilet`)
2. Tokenize into slots
3. Encode to hex
4. Decode back to slots
5. Render into a readable sentence

---

## ⚙️ Dictionaries

All slot values live in `dict/` as JSON files. Each key is a hexcode, each value is a lowercase word.

Example `verbs.json`:

```json
{
  "000001": "install",
  "000002": "remove",
  "000003": "inspect"
}
```

Want to add words? Just expand the dicts — no retraining or retriggering needed.

---

## 💡 Design Philosophy

- **Human in, byte out.**
- Fast, fixed-width slot schema (no fluff).
- Zero AI needed to decode — works offline.
- GPT-friendly: small enough to pass as tokens, structured enough to prompt.

---

## 🛣️ Roadmap

- [x] Fuzzy normalization (`copperr` → `copper`)
- [x] 16-slot architecture complete
- [ ] Contextual inference for conflicting tokens (e.g. `leak` as cause vs. object)
- [ ] Event/chaincode integration
- [ ] GUI playground / mobile app

---

## 🧠 Credits

Created by JD of JD Plumbing SoFlo  
Powered by domain-first logic, not NLP spaghetti.

---

## 🔖 License

MIT, or possibly Just Don't Be Evil.
