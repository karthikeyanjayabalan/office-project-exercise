import sqlite3

DB_NAME = "office_tasks.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("Initializing 'people' table structure...")
    # Table schema matching your explicit person criteria
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        random_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
    print("Database ready.")

if __name__ == "__main__":
    init_database()
