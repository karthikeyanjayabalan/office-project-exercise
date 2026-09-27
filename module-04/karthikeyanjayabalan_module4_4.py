import sqlite3

DB_NAME = "office_tasks.db"

def view_people_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # 1. Added missing_field to the query, and kept the +4 hours timezone correction
        cursor.execute("SELECT id, name, phone_number, random_id, missing_field, datetime(created_at, '+4 hours') FROM people;")
        rows = cursor.fetchall()
        
        # 2. Expanded row layout formatting widths to include the missing tracking column cleanly
        row_layout = "{:<4} | {:<12} | {:<15} | {:<10} | {:<13} | {}"
        
        print("\n" + "=" * 95)
        print(row_layout.format("ID", "NAME", "PHONE NUMBER", "RANDOM ID", "MISSING FIELD", "LOCAL CREATED AT"))
        print("=" * 95)
        
        for row in rows:
            # 3. Bulletproof loop: Convert database NULL/None cells cleanly to empty text "" so formatting won't crash
            safe_row = [str(item) if item is not None else "" for item in row]
            print(row_layout.format(*safe_row))
            
        print("=" * 95 + "\n")
        
    except sqlite3.OperationalError as e:
        print(f"Error reading 'people' table structure: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    view_people_table()



# import sqlite3

# DB_NAME = "office_tasks.db"

# def view_people_table():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
    
#     try:
#         # Convert UTC storage timestamps (+4 hours) to match your local timezone
#         cursor.execute("SELECT id, name, phone_number, random_id, datetime(created_at, '+4 hours') FROM people;")
#         rows = cursor.fetchall()
        
#         # Explicit horizontal character alignments preventing column drifting
#         row_layout = "{:<4} | {:<10} | {:<15} | {:<12} | {}"
        
#         print("\n" + "=" * 80)
#         print(row_layout.format("ID", "NAME", "PHONE NUMBER", "RANDOM ID", "LOCAL CREATED AT"))
#         print("=" * 80)
        
#         for row in rows:
#             print(row_layout.format(row[0], row[1], row[2], row[3], row[4]))
            
#         print("=" * 80 + "\n")
        
#     except sqlite3.OperationalError as e:
#         print(f"Error reading 'people' table structure: {e}")
#     finally:
#         conn.close()

# if __name__ == "__main__":
#     view_people_table()
