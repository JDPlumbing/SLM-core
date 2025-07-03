const sqlite3 = require('sqlite3').verbose();

// Open the database
const db = new sqlite3.Database('./dictionaries.db');

// Query the database for all dictionary entries
db.all('SELECT * FROM dictionaries', [], (err, rows) => {
  if (err) {
    throw err;
  }
  console.log("All dictionary entries:");
  rows.forEach((row) => {
    console.log(`${row.word}: ${row.definition}`);
  });
});

// Close the database connection
db.close();
