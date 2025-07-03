const sqlite3 = require('sqlite3').verbose();

// Open the database
const db = new sqlite3.Database('./dictionaries.db');

// Function to insert data into the dictionary table
const insertData = (word, definition) => {
  db.run(
    `INSERT INTO dictionaries (word, definition) VALUES (?, ?)`,
    [word, definition],
    function (err) {
      if (err) {
        console.error("Error inserting data: ", err);
      } else {
        console.log(`Added ${word} to the dictionary.`);
      }
    }
  );
};

// Insert some example data
insertData('plumber', 'A person who installs or repairs piping systems.');
insertData('pipe', 'A tube used to convey fluids or gases.');

// Close the database connection
db.close();
