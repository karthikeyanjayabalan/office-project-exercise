# import sqlite3
# from karthikeyanjayabalan_mod04_ex04_view import view_people_table

# DB_NAME = "office_tasks.db"

# def delete_row_by_id(target_id):
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
    
#     # SQL query targeting the exact row ID
#     delete_query = "DELETE FROM people WHERE id = ?;"
    
#     try:
#         print(f"\nAttempting to delete record with ID: {target_id}...")
        
#         # Execute deletion command
#         cursor.execute(delete_query, (target_id,))
#         conn.commit()
        
#         # Check if a row was actually deleted
#         if cursor.rowcount > 0:
#             print(f"Success! Row ID {target_id} has been permanently removed.")
#         else:
#             print(f"Notice: No record found with ID {target_id}. No rows were modified.")
        
#         # Display the updated database table grid
#         print("\n--- Displaying Updated Database State ---")
#         view_people_table()
        
#     except sqlite3.OperationalError as e:
#         print(f"Database operational failure: {e}")
#     finally:
#         conn.close()

# if __name__ == "__main__":
#     # 📌 CHANGE THIS NUMBER to whatever specific row ID you want to delete
#     ID_TO_DELETE = 1000
    
#     delete_row_by_id(ID_TO_DELETE)




# import sqlite3
# from karthikeyanjayabalan_mod04_ex04_view import view_people_table

# DB_NAME = "office_tasks.db"

# def delete_records_above_seven():
#     conn = sqlite3.connect(DB_NAME)
#     cursor = conn.cursor()
    
#     # SQL Command to wipe any rows with a primary ID higher than 7
#     delete_query = "DELETE FROM people WHERE id > 7;"
    
#     try:
#         print("\nInitializing row truncation process for IDs greater than 7...")
        
#         # 1. Execute the deletion query
#         cursor.execute(delete_query)
#         conn.commit()
        
#         # 2. Get the count of remaining rows to verify database impact
#         cursor.execute("SELECT COUNT(*) FROM people;")
#         remaining_count = cursor.fetchone()[0]
        
#         print(f"Truncation Complete! Your database now has exactly {remaining_count} records left.")
        
#         # 3. Display the final cleaned table matrix layout
#         print("\n--- Displaying Final Core Database State ---")
#         view_people_table()
        
#     except sqlite3.OperationalError as e:
#         print(f"Database modification failure: {e}")
#     finally:
#         conn.close()

# if __name__ == "__main__":
#     delete_records_above_seven()
