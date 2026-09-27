import sqlite3

DB_NAME = "office_tasks.db"
ROW_LAYOUT = "{:<4} | {:<12} | {:<15} | {:<10} | {:<13}"

def search_people_by_name(search_term: str):
    """Searches names inside the people table using fuzzy wildcard matching."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = "SELECT id, name, phone_number, random_id, missing_field FROM people WHERE name LIKE ?;"
    formatted_pattern = f"%{search_term}%"
    
    try:
        cursor.execute(query, (formatted_pattern,))
        results = cursor.fetchall()
        
        print("\n" + "=" * 70)
        print(f" SEARCH SYSTEM RESULTS FOR QUERY TERM: '{search_term}'")
        print("=" * 70)
        
        if not results:
            print(" No matches found for this criteria statement.")
        else:
            print(ROW_LAYOUT.format("ID", "NAME", "PHONE NUMBER", "RANDOM ID", "MISSING FIELD"))
            print("-" * 70)
            for row in results:
                # Converts any None/Null cells to an empty string safely before printing
                safe_row = [str(item) if item is not None else "" for item in row]
                print(ROW_LAYOUT.format(*safe_row))
                
        print("=" * 70 + "\n")
        return results
        
    except sqlite3.OperationalError as e:
        print(f"Search index operational failure: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Test Case 1: Searching for your original rows
    search_people_by_name("karthik")
    
    # Test Case 2: Searching for your new Swagger row
    search_people_by_name("denver")


# import sqlite3

# DB_NAME = "office_tasks.db"
# ROW_LAYOUT = "{:<4} | {:<12} | {:<15} | {:<10} | {:<13}"

# def search_people_by_name(search_term: str):
#     """Searches names inside the people table using fuzzy wildcard matching."""
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
    
#     # Using SQL LIKE syntax with percentage signs to catch partial substring strings
#     query = "SELECT id, name, phone_number, random_id, missing_field FROM people WHERE name LIKE ?;"
#     formatted_pattern = f"%{search_term}%"
    
#     try:
#         cursor.execute(query, (formatted_pattern,))
#         results = cursor.fetchall()
        
#         print("\n" + "=" * 70)
#         print(f" SEARCH SYSTEM RESULTS FOR QUERY TERM: '{search_term}'")
#         print("=" * 70)
        
#         if not results:
#             print(" No matches found for this criteria statement.")
#         else:
#             print(ROW_LAYOUT.format("ID", "NAME", "PHONE NUMBER", "RANDOM ID", "MISSING FIELD"))
#             print("-" * 70)
#             for row in results:
#                 # print(ROW_LAYOUT.format(row, row, row, row, row))
#                 print(ROW_LAYOUT.format(*row))
                
#         print("=" * 70 + "\n")
#         return results
        
#     except sqlite3.OperationalError as e:
#         print(f"Search index operational failure: {e}")
#     finally:
#         conn.close()

# if __name__ == "__main__":
#     # Test Case 1: Searching for letters present in multiple rows
#     search_people_by_name("karthik")
    
#     # Test Case 2: Searching for an explicit row fragment
#     search_people_by_name("bravo")
#     search_people_by_name("charlie")
