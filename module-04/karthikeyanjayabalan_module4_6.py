import sqlite3
import random
import string

DB_NAME = "office_tasks.db"

def alter_schema_and_populate():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:                
        # 1. Add the column named 'missing_field' to your existing 'people' table blueprint
        print("Altering table schema to add 'missing_field' column...")
        cursor.execute("ALTER TABLE people ADD COLUMN missing_field TEXT;")
        conn.commit()
        print("Column 'missing_field' added successfully.")
    except sqlite3.OperationalError:
        # Prevents crashing if the script is run a second time
        print("Column 'missing_field' already exists in schema. Continuing to population step.")
        
    try:
        # 2. Retrieve all current primary keys to assign individual characters
        cursor.execute("SELECT id FROM people;")
        row_ids = [row[0] for row in cursor.fetchall()]
        
        print(f"Populating {len(row_ids)} rows with random single characters...")
        
        # 3. Iterate through every record and update it with a random uppercase letter
        for row_id in row_ids:
            random_char = random.choice(string.ascii_uppercase)
            cursor.execute("UPDATE people SET missing_field = ? WHERE id = ?;", (random_char, row_id))
            
        conn.commit()
        print("All rows backfilled successfully.")
        
        # 4. View results right inside the terminal to check the data state
        cursor.execute("SELECT id, name, phone_number, random_id, missing_field FROM people;")
        updated_rows = cursor.fetchall()
        
        layout = "{:<4} | {:<12} | {:<15} | {:<10} | {:<13}"
        print("\n" + "=" * 65)
        print(layout.format("ID", "NAME", "PHONE NUMBER", "RANDOM ID", "MISSING FIELD"))
        print("=" * 65)
        for row in updated_rows:
            print(layout.format(row[0], row[1], row[2], row[3], row[4]))
        print("=" * 65 + "\n")
        
    except sqlite3.OperationalError as e:
        print(f"Operational failure updating entries: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    alter_schema_and_populate()
