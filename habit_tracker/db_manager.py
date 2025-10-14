import sqlite3
from pathlib import Path
from datetime import date

# Define the path to the database file relative to the project root
DB_PATH = Path(__file__).resolve().parent.parent / "db" / "habits.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True) # Ensure the 'db' directory exists

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    return conn

def init_db():
    """Initializes the database by creating the necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create the 'habits' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'archived')),
        periodicity TEXT NOT NULL DEFAULT 'daily'
    );
    """)

    # Create the 'completions' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS completions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        completed_at DATE NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
    );
    """)
    
    # Add a unique constraint to prevent duplicate completions for the same habit on the same day
    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_habit_date ON completions (habit_id, completed_at);
    """)
    
    conn.commit()
    conn.close()

def add_habit(name: str, description: str = ""):
    """Adds a new habit to the database."""
    conn = get_db_connection()
    conn.execute("INSERT INTO habits (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

def get_habits(status: str = 'active'):
    """
    Retrieves habits from the database based on their status.
    :param status: 'active', 'archived', or 'all'
    """
    conn = get_db_connection()
    if status == 'all':
        habits = conn.execute("SELECT * FROM habits ORDER BY created_at").fetchall()
    else:
        habits = conn.execute("SELECT * FROM habits WHERE status = ? ORDER BY created_at", (status,)).fetchall()
    conn.close()
    return habits

def update_habit_status(habit_id: int, new_status: str):
    """Updates the status of a habit (e.g., 'active' or 'archived')."""
    conn = get_db_connection()
    conn.execute("UPDATE habits SET status = ? WHERE id = ?", (new_status, habit_id))
    conn.commit()
    conn.close()

def delete_habit(habit_id: int):
    """Deletes a habit and its associated completions from the database."""
    conn = get_db_connection()
    conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
    conn.commit()
    conn.close()

def add_completion(habit_id: int, completion_date: date):
    """Adds a completion record for a habit on a specific date."""
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)", (habit_id, completion_date))
        conn.commit()
    except sqlite3.IntegrityError:
        # This error occurs if the unique constraint (habit_id, completed_at) is violated.
        # It means the habit is already marked as done for that day.
        pass
    finally:
        conn.close()

def get_completions(habit_id: int):
    """Retrieves all completion dates for a specific habit."""
    conn = get_db_connection()
    completions = conn.execute("SELECT completed_at FROM completions WHERE habit_id = ? ORDER BY completed_at DESC", (habit_id,)).fetchall()
    conn.close()
    return [row['completed_at'] for row in completions]
