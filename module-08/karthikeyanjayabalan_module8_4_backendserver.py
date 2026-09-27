import sqlite3
import random
import threading
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastmcp import FastMCP

# Synchronized relative path mapping to ensure shared access with the frontend
DB_NAME = "./mcp_application.db"

# =========================================================================
# 🏗️ SUBSYSTEM 1: SQLITE PERSISTENT DATABASE ENGINE (Syllabus Requirement 1)
# =========================================================================
def init_application_database():
    """Builds the profile database layout automatically if missing."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mcp_app_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        user_key TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def insert_profile_record(name: str, phone: str) -> dict:
    """Commits extracted parameters into SQL rows with a randomized tracking key."""
    generated_user_key = f"KEY-{random.randint(10000, 99999)}"
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mcp_app_data (name, phone, user_key) VALUES (?, ?, ?);",
        (name.strip(), phone.strip(), generated_user_key)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "name": name, "phone": phone, "user_key": generated_user_key}

def search_database_by_name(target_name: str) -> str:
    """Fuzzy name lookup function that acts as the data retrieval layer for MCP."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, user_key FROM mcp_app_data WHERE name LIKE ?;", (f"%{target_name}%",))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"Query Notice: No database records matching name search pattern '{target_name}' were found."
        
    log_blocks = [f"Found {len(rows)} matching profile record(s):"]
    for row in rows:
        # Unwraps individual tuple locations (0, 1, 2, 3) from the SQL matrix response array
        log_blocks.append(f"Record Key ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | User Key ID: {row[3]}")
    return "\n".join(log_blocks)

# Self-initialize storage parameters immediately on boot
init_application_database()

# =========================================================================
# 🤖 SUBSYSTEM 2: MODEL CONTEXT PROTOCOL (MCP) SERVER BRIDGE (Syllabus Requirement 2)
# =========================================================================
mcp_server = FastMCP("App Core Database Bridge")

@mcp_server.tool()
def search_mcp_database(target_name: str) -> str:
    """Exposes a secure tool allowing connected clients to fetch factual database details."""
    return search_database_by_name(target_name)

# =========================================================================
# 🌐 SUBSYSTEM 3: FASTAPI PROGRAMMATIC REST API GATEWAY (Syllabus Requirement 2)
# =========================================================================
api_app = FastAPI(title="Integrated Application DB API Portal")

@api_app.post("/register")
def register_user_endpoint(payload: dict):
    """Programmatic API connector endpoint to add records directly to SQL rows."""
    try:
        name = payload.get("name")
        phone = payload.get("phone")
        if not name or not phone:
            raise HTTPException(status_code=400, detail="Missing name or phone parameter in payload")
            
        record = insert_profile_record(name, phone)
        return {"status": "Success", "message": "Information safely stored!", "data": record}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_app.get("/mcp-search")
def api_mcp_search_endpoint(name: str):
    """Exposes the internal database-to-MCP connection parameters over an HTTP path query."""
    try:
        return {"status": "Success", "mcp_context": search_database_by_name(name)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Spawn the background protocol thread loop for FastMCP internally
    mcp_worker = threading.Thread(target=mcp_server.run, daemon=True)
    mcp_worker.start()
    
    # Run public API layer on primary server port 8000
    print("🌐 Starting Backend Services on port 8000...")
    print("🤖 Model Context Protocol Server is actively tracking queries on sub-threads...")
    uvicorn.run(api_app, host="127.0.0.1", port=8888)
