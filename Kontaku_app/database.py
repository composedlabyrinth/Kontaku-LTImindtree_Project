import sqlite3

class Database:
    def __init__(self, db_file="contacts.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the contacts table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                address TEXT,
                category TEXT
            )
        """)
        self.conn.commit()

    def add_contact(self, name, phone, email, address, category):
        """Insert a new contact."""
        self.cursor.execute("INSERT INTO contacts (name, phone, email, address, category) VALUES (?, ?, ?, ?, ?)",
                            (name, phone, email, address, category))
        self.conn.commit()

    def fetch_contacts(self):
        """Return all contacts sorted by name (Case Insensitive)."""
        self.cursor.execute("SELECT * FROM contacts ORDER BY name COLLATE NOCASE ASC")
        return self.cursor.fetchall()
    
    def fetch_by_category(self, category):
        """Return contacts filtered by category, sorted by name (Case Insensitive)."""
        self.cursor.execute("SELECT * FROM contacts WHERE category=? ORDER BY name COLLATE NOCASE ASC", (category,))
        return self.cursor.fetchall()

    def remove_contact(self, id):
        """Delete a contact by ID."""
        self.cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
        self.conn.commit()

    def update_contact(self, id, name, phone, email, address, category):
        """Update an existing contact."""
        self.cursor.execute("""
            UPDATE contacts 
            SET name=?, phone=?, email=?, address=?, category=? 
            WHERE id=?
        """, (name, phone, email, address, category, id))
        self.conn.commit()

    def search_contacts(self, query):
        """Search contacts sorted by name (Case Insensitive)."""
        self.cursor.execute("SELECT * FROM contacts WHERE name LIKE ? OR phone LIKE ? ORDER BY name COLLATE NOCASE ASC", 
                            ('%' + query + '%', '%' + query + '%'))
        return self.cursor.fetchall()

    def contact_exists(self, name):
        """Check if a contact with the given name already exists (case-insensitive)."""
        self.cursor.execute("SELECT 1 FROM contacts WHERE name = ? COLLATE NOCASE", (name,))
        return self.cursor.fetchone() is not None

    def __del__(self):
        """Close connection when object is destroyed."""
        if self.conn:
            self.conn.close()