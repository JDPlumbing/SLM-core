
"""
README — SLM Tokenizer v7
=========================

This tokenizer parses natural language into structured SLM slot entries for downstream use. It is fully deterministic, greedy (left-to-right), and prefix-driven. No NLP or dependency trees. Just clean matching.

Slot Schema:
------------
- subject
- verb
- object
- location
- intent
- cause
- status
- adverb

Prefix Rules:
-------------
- **Single-symbol prefixes** (`!`, `#`, `~`, etc.) are used **only for 2-word entries** like `!water_heater` or `~did_replace`
- **Double-symbol prefixes** (`!!`, `##`, `~~`, etc.) are used **only for 1-word entries** like `!!plumber` or `##dishwasher`

Tokenizer Logic:
----------------
1. **First pass**: scan for 2-word matches (e.g. `water_heater`) and match against the single-symbol prefixed dictionary entries (e.g. `#water_heater`)
2. **Second pass**: scan remaining orphan words and match against double-symbol entries (e.g. `##heater`)
3. **Subject fallback**: if no subject is matched, defaults to `!!someone`

Dictionaries:
-------------
- Stored in `/dicts/{slot}.txt`
- Each entry must start with the correct prefix
- Do **not** mix single and double prefix styles — enforce prefix rules above

Example:
--------
Sentence:
    "The plumber did fix the rusty pipe to address the leak"

Output:
    !!plumber ~did_fix #rusty_pipe >>leak

That’s your full raw match, machine-readable and human-legible.

Use Cases:
----------
- Translating job logs
- Building chaincode capsules
- Structured tagging of task and action data

"""
