const sqlite3 = require('sqlite3').verbose();

// Open the database (will create the file if it doesn't exist)
const db = new sqlite3.Database('./dictionaries.db');

// Create a table for storing dictionary entries
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS dictionaries (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      word TEXT NOT NULL,
      definition TEXT NOT NULL
    );
  `);

  console.log("Table 'dictionaries' created or verified.");
});

// Close the database connection
db.close();
