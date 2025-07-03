-- schema.sql
CREATE TABLE IF NOT EXISTS dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slot TEXT NOT NULL,        -- e.g., 'verb', 'color'
    word TEXT NOT NULL UNIQUE  -- e.g., 'install'
);

CREATE INDEX IF NOT EXISTS idx_slot_word ON dictionary(slot, word);
