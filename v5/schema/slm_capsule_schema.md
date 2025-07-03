# SLM Capsule Format Schema

## Total Size: 32 bytes

### Header (2 bytes / 16 bits):
- `version`: 4 bits – Schema version
- `clause_a_mask`: 4 bits – Slot presence bitmask for Clause A
- `clause_b_mask`: 4 bits – Slot presence bitmask for Clause B
- `context`: 4 bits – Domain, priority, or other context

### Clause A & B (14 bytes each / 112 bits):
- `subject`: 10 bits – up to 1024 values x
- `verb`: 14 bits – up to 16384 values x
- `object`: 14 bits – up to 16384 values x
- `modifier`: 10 bits – up to 1024 values
- `location`: 10 bits – up to 1024 values x
- `intent`: 12 bits – up to 4096 values x
- `cause`: 12 bits – up to 4096 values x
- `status`: 10 bits – up to 1024 values
- `adverb`: 10 bits – up to 1024 values

### Footer (2 bytes / 16 bits):
- `checksum`: 16 bits – Optional CRC, signature, or chain tag