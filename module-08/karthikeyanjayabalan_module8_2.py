import sqlite3
from fastmcp import FastMCP

# Initialize an MCP server instance specifically optimized for database connections
mcp = FastMCP("Database Protocol Server")

# Update this path string to target your Module 6 structural profile database file
DB_PATH = "../module-06/structured_userdata.db"

# 🛠️ MCP TOOL: Reading directly from SQLite database rows
@mcp.tool()
def fetch_latest_database_records(limit: int = 5) -> str:
    """Useful for retrieving the most recent user profile records logged inside the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Pull rows sorted by the unique incremental primary key ID
        query = f"SELECT id, extracted_name, extracted_time, extracted_number FROM structured_profiles ORDER BY id DESC LIMIT ?;"
        cursor.execute(query, (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "Database check complete: The structured_profiles table is currently empty."
            
        # Format the fetched rows into a clean, text-scannable data log block
        result_blocks = ["--- [SQLITE DATABASE EXTRACED RECORDS] ---"]
        for row in rows:
            result_blocks.append(f"ID: {row[0]} | Name: {row[1]} | Time: {row[2]} | Number: {row[3]}")
            
        return "\n".join(result_blocks)
        
    except sqlite3.OperationalError as e:
        return f"Database Error: Could not connect or query file path. Details: {e}. Check if the database file exists."

if __name__ == "__main__":
    mcp.run()
