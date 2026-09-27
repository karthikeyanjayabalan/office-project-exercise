import sqlite3
import time
# Import your Exercise 04 function to show database state changes live
from karthikeyanjayabalan_mod04_ex04_view import view_people_table

DB_NAME = "office_tasks.db"

def adjust_and_forget(target_id=7):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # 1. Fetch the historical name state to hold in memory
        cursor.execute("SELECT name FROM people WHERE id = ?;", (target_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"Error: Row ID {target_id} not found in database. Add data first.")
            return
            
        original_name = result[0]
        print(f"\n[Step 1] original state captured for ID {target_id}: '{original_name}'")
        
        # 2. Modify the row data value to a temporary state
        temp_name = "TEMP_KJ"
        cursor.execute("UPDATE people SET name = ? WHERE id = ?;", (temp_name, target_id))
        conn.commit()
        print(f"[Step 2] Temporarily updated ID {target_id} name value to: '{temp_name}'")
        
        # Display the modified state immediately using your visual matrix
        print("\n--- Live Check: Showing Changed State in Table ---")
        view_people_table()
        
        # 3. Hold execution state for exactly 15 seconds
        print("Pausing execution for 15 seconds. Reverting back soon...")
        for remaining in range(15, 0, -1):
            print(f"Time remaining: {remaining} seconds...", end="\r")
            time.sleep(1)
        print("\nTime's up! Initializing automatic database rollback event...")
        
        # 4. Revert the database row back to its initial value
        cursor.execute("UPDATE people SET name = ? WHERE id = ?;", (original_name, target_id))
        conn.commit()
        print(f"[Step 3] Successfully reverted ID {target_id} back to original: '{original_name}'")
        
        # Display final state to confirm clean restoration
        print("\n--- Live Check: Showing Restored State in Table ---")
        view_people_table()
        
    except sqlite3.OperationalError as e:
        print(f"Database adjustment event failure: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    adjust_and_forget()
