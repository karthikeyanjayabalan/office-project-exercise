import sqlite3
from karthikeyanjayabalan_mod04_ex04_view import view_people_table

DB_NAME = "office_tasks.db"

def clear_duplicate_records():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # SQL logic: Delete rows where there is another row with the same name 
    # and phone number, but with a smaller (older) unique ID.
    delete_query = """
    DELETE FROM people
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM people
        GROUP BY name, phone_number
    );
    """
    
    try:
        print("\nChecking database file for duplicate rows...")
        
        # 1. Check how many records exist before the deduplication process
        cursor.execute("SELECT COUNT(*) FROM people;")
        count_before = cursor.fetchone()[0]
        
        # 2. Run the deletion query execution block
        cursor.execute(delete_query)
        conn.commit()
        
        # 3. Check how many records remain
        cursor.execute("SELECT COUNT(*) FROM people;")
        count_after = cursor.fetchone()[0]
        
        removed_count = count_before - count_after
        print(f"Cleanup Complete! Safely removed {removed_count} duplicate rows from the table.")
        
        # 4. Display the clean database grid layout
        print("\n--- Displaying Cleaned Dataset Matrix ---")
        view_people_table()
        
    except sqlite3.OperationalError as e:
        print(f"Database operational adjustment crash: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clear_duplicate_records()
