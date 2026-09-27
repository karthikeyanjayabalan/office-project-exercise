import sqlite3
import random
import threading
import requests
import json
import uvicorn
import streamlit as st
from fastapi import FastAPI, HTTPException
from fastmcp import FastMCP

# Core System Connectivity Parameters
DB_NAME = "./mcp_application.db"
MODEL_NAME = "llama3.2:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"

# =========================================================================
# 🏗️ BACKEND DATA STRUCTURE SETUP
# =========================================================================
def init_application_database():
    """Initializes the persistent profile storage tracking table inside SQLite if missing."""
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
    # Seed a clean sample record if the data table is completely empty
    cursor.execute("SELECT COUNT(*) FROM mcp_app_data;")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO mcp_app_data (name, phone, user_key) VALUES (?, ?, ?);",
            ("David", "055-778899", "KEY-71249")
        )
    conn.commit()
    conn.close()

def search_database_by_name(target_name: str) -> str:
    """Queries SQL rows using fuzzy string matching patterns to retrieve records."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, user_key FROM mcp_app_data WHERE name LIKE ?;", (f"%{target_name}%",))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return f"Query Notice: No database records matching name search pattern '{target_name}' were found."
        
    log_blocks = [f"Found {len(rows)} matching profile record(s):"]
    for row in rows:
        log_blocks.append(f"Record Key ID: {row[0]} | Name: {row[1]} | Phone: {row[2]} | User Key ID: {row[3]}")
    return "\n".join(log_blocks)

# Boot up database mapping arrays immediately
init_application_database()

# =========================================================================
# 🤖 REQUIREMENT 1: CREATE AN API TO CONNECT MCP SERVER WITH SQL DATABASE
# =========================================================================
# 1. Initialize the Model Context Protocol Server Bridge
mcp_server = FastMCP("App Core Database Bridge")

@mcp_server.tool()
def search_mcp_database(target_name: str) -> str:
    """Exposes a secure tool allowing connected clients to fetch factual database details."""
    return search_database_by_name(target_name)

# 2. Wrap the protocol engine layer inside a programmatic FastAPI HTTP gateway
api_gateway = FastAPI(title="Integrated Application DB API Portal")

@api_gateway.get("/mcp-search")
def api_mcp_search_endpoint(name: str):
    """Programmatic API connector endpoint that maps incoming web requests straight to the MCP SQL tool."""
    try:
        facts_context = search_database_by_name(name)
        return {"status": "Success", "connected_mcp_tool_context": facts_context}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_backend_infrastructure_loop():
    """Hosts your public API gateway and background MCP channels concurrently on port 8888."""
    # Spawn the FastMCP stdio/sse channel loop inside an asynchronous worker sub-thread
    mcp_worker = threading.Thread(target=mcp_server.run, daemon=True)
    mcp_worker.start()
    
    # Launch Uvicorn REST services directly on port 8888
    uvicorn.run(api_gateway, host="127.0.0.1", port=8888, log_level="warning")


# =========================================================================
# 🤖 REQUIREMENT 2: CONNECT THE MCP SERVER WITH AN LLM TO RESPOND ABOUT DATABASE
# =========================================================================
def run_streamlit_interface():
    st.set_page_config(page_title="Intelligent Core Application", layout="centered")
    st.title("🧠 Intelligent LLM Database Core Application")
    st.write("Interact with your local database using plain English conversation to retrieve facts or save information.")
    st.write("🌐 *Application REST API connector listening live on gateway:* `http://127.0.0.1:8888`")
    st.divider()

    st.subheader("🔍 Grounded Intelligence Knowledge Search")
    search_name = st.text_input("Name Context Parameter (Fuzzy Search Target):", placeholder="Example: David")
    question = st.text_input("Your Question about the Database:", placeholder="Example: What is David's user key allocation?")
    
    if st.button("Ask LLM Engine", type="primary"):
        if not search_name.strip() or not question.strip():
            st.warning("Please fill out both field parameters.")
        else:
            with st.spinner("MCP is fetching context facts over API connector..."):
                try:
                    # 1. Pull facts by programmatically invoking our custom connected REST path query
                    api_res = requests.get("http://127.0.0", params={"name": search_name})
                    api_res.raise_for_status()
                    mcp_facts = api_res.json()["connected_mcp_tool_context"]
                    
                    # 2. Enrich prompt and pass to local model to guarantee an un-hallucinated answer
                    enriched_prompt = (
                        "You are an intelligent database core administrator. "
                        "Answer the user's question using ONLY the following verified database facts provided by the MCP server tools.\n\n"
                        f"MCP Server Facts Context:\n{mcp_facts}\n\n"
                        f"User Question: {question}"
                    )
                    
                    response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": enriched_prompt, "stream": False})
                    response.raise_for_status()
                    ai_reply = response.json().get("response", "").strip()
                    
                    # Render outputs beautifully onto the UI canvas grid
                    st.markdown("### 📋 MCP Context Retrieved via API:")
                    st.info(mcp_facts)
                    st.markdown("### 💡 LLM Grounded Answer:")
                    st.write(ai_reply)
                    
                except Exception as e:
                    st.error(f"Error querying connected backend pipeline: {e}")

# =========================================================================
# 🚀 CORE ORCHESTRATION LAYER
# =========================================================================
if st.runtime.exists():
    # If the file is triggered inside the active Streamlit engine path, render the frontend
    run_streamlit_interface()
else:
    # If executed directly via 'py script.py' from terminal line:
    if __name__ == "__main__":
        # Spawn backend infrastructure loop on a daemon thread
        backend_thread = threading.Thread(target=run_backend_infrastructure_loop, daemon=True)
        backend_thread.start()
        
        # Use shell execution to cleanly invoke the Streamlit app wrapper on an independent port
        print("🌐 Starting Integrated Application Backend Services on port 8888...")
        print("Launching graphical UI view interface workspace...")
        import subprocess
        subprocess.run("py -m streamlit run karthikeyanjayabalan_mod08_ex04_myapp.py --server.port 8555 --server.fileWatcherType none", shell=True)
