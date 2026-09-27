import sqlite3

# Connect to the database
conn = sqlite3.connect("office_tasks.db")
cursor = conn.cursor()

try:
    # Query all columns from the tasks table
    cursor.execute("SELECT * FROM tasks;")
    rows = cursor.fetchall()
    
    print("\n" + "="*70)
    print(f"{'ID':<4} | {'TITLE':<25} | {'STATUS':<15} | {'CREATED AT'}")
    print("="*70)
    
    for row in rows:
        # row[0]=id, row[1]=title, row[2]=description, row[3]=status, row[4]=created_at
        print(f"{row[0]:<4} | {row[1]:<25} | {row[3]:<15} | {row[4]}")
    print("="*70 + "\n")

except sqlite3.OperationalError as e:
    print(f"Error: Could not read table. Make sure the database file name is exact. Details: {e}")

finally:
    conn.close()
