# SLM v5

A clean, fixed-length 32-byte protocol for encoding structured human intent.

## Layout

- 2 bytes: header (version, slot flags, domain)
- 14 bytes: clause A
- 14 bytes: clause B
- 2 bytes: footer (checksum or tag)

## Goals

- Fully deterministic
- Fits in radio/micro/sensor transmission
- Reversible from capsule → meaning
