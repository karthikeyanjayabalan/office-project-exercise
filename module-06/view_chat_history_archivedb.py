import sqlite3

DB_NAME = "chat_history_archive.db"

def view_archived_chat_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        # Convert UTC storage timestamps (+4 hours) to match your local timezone
        query = """
        SELECT id, user_question, ai_response, datetime(timestamp, '+4 hours') 
        FROM chat_logs 
        ORDER BY id ASC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        # Explicit horizontal spacing to prevent column drifting with long conversations
        # Truncates long AI responses in the preview grid to keep the console clean
        row_layout = "{:<4} | {:<25} | {:<30} | {}"
        
        print("\n" + "=" * 90)
        print(row_layout.format("ID", "USER QUESTION", "AI RESPONSE PREVIEW", "LOCAL TIMESTAMP"))
        print("=" * 90)
        
        for row in rows:
            # Clean preview formatting: limit long multi-line AI strings to 30 characters
            clean_question = row[1][:22] + "..." if len(row[1]) > 22 else row[1]
            clean_response = row[2].replace('\n', ' ')[:27] + "..." if len(row[2]) > 27 else row[2]
            
            print(row_layout.format(row[0], clean_question, clean_response, row[3]))
            
        print("=" * 90 + "\n")
        
    except sqlite3.OperationalError as e:
        print(f"❌ Error reading table layout from '{DB_NAME}': {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    view_archived_chat_logs()
