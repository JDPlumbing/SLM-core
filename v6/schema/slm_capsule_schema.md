# SLM v6.1 Capsule Schema

A clean, fixed-length **36-byte** protocol for encoding structured semantic clauses.

## 🧱 Layout

- **Header**: 2 bytes (16 bits)
- **Clause A**: 16 bytes (8 slots × 2 bytes)
- **Clause B**: 16 bytes (8 slots × 2 bytes)
- **Footer**: 2 bytes (checksum or chainref)

---

## 🧩 Header (2 bytes / 16 bits)
| Field          | Bits | Description                       |
|----------------|------|-----------------------------------|
| `version`      | 4    | Capsule schema version            |
| `clause_a_mask`| 4    | Slot presence bitmask (Clause A)  |
| `clause_b_mask`| 4    | Slot presence bitmask (Clause B)  |
| `context`      | 4    | Domain, priority, or other use    |

---

## 🧠 Clause A & Clause B (16 bytes each / 128 bits)

Each clause holds **8 slots**, each encoded as a **16-bit unsigned int** (2 bytes).

| Slot       | Bits | Description                          |
|------------|------|--------------------------------------|
| `subject`  | 16   | Actor or initiator                   |
| `verb`     | 16   | Main action or behavior              |
| `object`   | 16   | Target or affected entity            |
| `location` | 16   | Spatial position or context          |
| `intent`   | 16   | Purpose or goal of the action        |
| `cause`    | 16   | Root cause or trigger                |
| `status`   | 16   | Current or resulting state           |
| `adverb`   | 16   | Manner, intensity, temporal nuance   |

**Note:** All entries must be exactly two words (snake_case), e.g. `he_installed`, `leaking_pipe`, `drains_quickly`.

---

## 🧾 Footer (2 bytes / 16 bits)

| Field       | Bits | Description                         |
|-------------|------|-------------------------------------|
| `checksum`  | 16   | Optional CRC, chainref, or signature|

---

## 🧬 Total: 36 Bytes = 288 Bits
- Header: 2 bytes
- Clause A: 16 bytes
- Clause B: 16 bytes
- Footer: 2 bytes

---

## 🎯 Design Goals
- Fully deterministic and reversible
- All slots aligned to 2-byte words
- No special-cased slot behavior
- Human-friendly rendering via 2-word overlap collapsing
- Future-proof: 65,536 values per slot
