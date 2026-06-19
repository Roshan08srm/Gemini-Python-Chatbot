import sqlite3

DB_FILE = "chats.db"

def init_db():
    """
    Initializes the SQLite database and creates the sessions and messages tables
    if they don't already exist. Includes a schema migration to add 'session_id'
    to the 'messages' table if it was created under the older single-session schema.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create sessions table first
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create messages table (using the new schema with nullable session_id initially for migration)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES sessions (id) ON DELETE CASCADE
        )
    """)
    
    # --- SCHEMA MIGRATION ---
    # If the user has an existing database from the older version, the 'messages' table
    # exists but lacks the 'session_id' column. We dynamically add it here.
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN session_id TEXT;")
    except sqlite3.OperationalError:
        # Column already exists, so no action is needed
        pass
        
    # Ensure there is a default session to link any orphaned/migrated messages to
    cursor.execute("INSERT OR IGNORE INTO sessions (id, title) VALUES ('default', 'Previous Chat')")
    
    # Set any NULL session_id fields to 'default'
    cursor.execute("UPDATE messages SET session_id = 'default' WHERE session_id IS NULL")
    
    conn.commit()
    conn.close()

def create_session(session_id: str, title: str = "New Chat"):
    """
    Inserts a new chat session into the sessions table.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO sessions (id, title) VALUES (?, ?)",
        (session_id, title)
    )
    conn.commit()
    conn.close()

def update_session_title(session_id: str, title: str):
    """
    Updates the display title of a specific chat session.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE sessions SET title = ? WHERE id = ?",
        (title, session_id)
    )
    conn.commit()
    conn.close()

def get_all_sessions():
    """
    Retrieves all sessions from the database ordered by creation time (newest first).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, created_at FROM sessions ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "title": row[1], "created_at": row[2]} for row in rows]

def save_message(session_id: str, role: str, content: str):
    """
    Saves a message associated with a specific chat session.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
        (session_id, role, content)
    )
    conn.commit()
    conn.close()

def load_messages(session_id: str):
    """
    Loads all messages for a specific session ordered by timestamp/ID.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"role": row[0], "content": row[1]} for row in rows]

def delete_session(session_id: str):
    """
    Deletes a specific session and all its messages.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()

def clear_all_db():
    """
    Clears all tables in the database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()
