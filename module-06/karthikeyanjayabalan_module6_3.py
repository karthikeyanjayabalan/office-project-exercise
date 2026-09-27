# py -m streamlit run .\karthikeyanjayabalan_module06_exercise03_llmdb.py --server.fileWatcherType none


import sqlite3
import datetime
import requests
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"
DB_NAME = "chat_history_archive.db"

st.set_page_config(page_title="LLM with SQLite DB Archive", layout="centered")
st.title("📊 Chat Engine with Database Archiving")
st.write("Every prompt and response is logged into a structured local SQLite database (`chat_history_archive.db`).")
st.divider()

# =========================================================================
# 🔄 PHASE 1: SQLITE LOGGING DATABASE INITIALIZATION
# =========================================================================
def init_log_database():
    """Builds the archive storage schema table automatically if missing."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_question TEXT NOT NULL,
        ai_response TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()

def log_chat_to_database(question: str, response: str):
    """Inserts a structured text row capturing the conversation text layers."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_logs (user_question, ai_response) VALUES (?, ?);",
        (question, response)
    )
    conn.commit()
    conn.close()

# Initialize the tracking schema on launch
init_log_database()

# =========================================================================
# 💬 PHASE 2: INTERACTIVE SCREEN RENDER RUNTIME
# =========================================================================
user_prompt = st.text_input("Ask a question to save to the database archive:", placeholder="Type your text query here...")

if st.button("Submit to AI & DB", type="primary"):
    if user_prompt.strip() == "":
        st.warning("Please enter a valid text question prompt first.")
    else:
        with st.spinner("AI is thinking and archiving details..."):
            payload = {
                "model": MODEL_NAME,
                "prompt": user_prompt.strip(),
                "stream": False
            }
            
            try:
                # 1. Execute standard HTTP API request to Ollama
                response = requests.post(OLLAMA_URL, json=payload)
                response.raise_for_status()
                
                result_data = response.json()
                ai_response_text = result_data.get("response", "").strip()
                
                # 2. DATABASE TRANSACTION STEP: Insert the text parameters permanently into SQLite
                log_chat_to_database(user_prompt.strip(), ai_response_text)
                
                # Render clean visual dashboard segments
                st.subheader("💡 AI Response:")
                st.info(ai_response_text)
                st.success("✅ Conversation log safely stored inside 'chat_history_archive.db'!")
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Ensure your local Ollama desktop background app is open!")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

# =========================================================================
# 📊 PHASE 3: SIDEBAR DATABASE HISTORICAL PANEL VIEW
# =========================================================================
st.sidebar.header("📜 Archived Database Logs")
if st.sidebar.button("Refresh Log Records", type="secondary"):
    st.rerun()

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Read rows and convert UTC storage timestamp (+4 hours) to match local timezone
    cursor.execute("SELECT id, user_question, ai_response, datetime(timestamp, '+4 hours') FROM chat_logs ORDER BY id DESC LIMIT 5;")
    logs = cursor.fetchall()
    conn.close()
    
    if not logs:
        st.sidebar.info("No logged transactions found yet.")
    else:
        for log in logs:
            st.sidebar.markdown(f"**ID: {log[0]}** | *{log[3]}*")
            st.sidebar.markdown(f"**Q:** {log[1]}")
            st.sidebar.markdown(f"**A:** {log[2][:60]}...")
            st.sidebar.divider()
except Exception:
    st.sidebar.error("Could not fetch archive logs.")
