import sqlite3

DB_NAME = "office_tasks.db"
ROW_LAYOUT = "{:<4} | {:<12} | {:<15} | {:<10} | {:<13}"

def approach_a_sql_sorting():
    """Approach 1: Let the SQL database engine compute the sort query directly."""
    print("\n" + "="*70)
    print(" APPROACH A: SORTED DIRECTLY BY THE SQL ENGINE (ORDER BY missing_field)")
    print("="*70)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    #  FIXED: Changed table target from 'tasks' to 'people'
    cursor.execute("SELECT id, name, phone_number, random_id, missing_field FROM people ORDER BY missing_field ASC;")
    rows = cursor.fetchall()
    
    print(ROW_LAYOUT.format("ID", "NAME", "PHONE NUMBER", "RANDOM ID", "MISSING FIELD"))
    print("-" * 70)
    for row in rows:
        print(ROW_LAYOUT.format(row[0], row[1], row[2], row[3], row[4]))
    
    conn.close()

def approach_b_python_sorting():
    """Approach 2: Fetch raw rows into Python memory and sort using custom lambda keys."""
    print("\n" + "="*70)
    print(" APPROACH B: FETCHED UNORDERED, SORTED IN PYTHON MEMORY (lambda)")
    print("="*70)
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    #  FIXED: Changed table target from 'tasks' to 'people'
    cursor.execute("SELECT id, name, phone_number, random_id, missing_field FROM people;")
    raw_rows = cursor.fetchall()  
    
    # Sort tuples in memory using index 4 (missing_field value)
    sorted_rows = sorted(raw_rows, key=lambda x: x[4])
    
    print(ROW_LAYOUT.format("ID", "NAME", "PHONE NUMBER", "RANDOM ID", "MISSING FIELD"))
    print("-" * 70)
    for row in sorted_rows:
        print(ROW_LAYOUT.format(row[0], row[1], row[2], row[3], row[4]))
        
    conn.close()

if __name__ == "__main__":
    approach_a_sql_sorting()
    approach_b_python_sorting()
