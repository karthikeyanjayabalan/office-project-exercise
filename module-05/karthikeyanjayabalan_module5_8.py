#py -m streamlit run .\karthikeyanjayabalan_mod05_ex06_chat.py

import json
import os
import requests
import streamlit as st

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:latest"
HISTORY_FILE = "chat_history.json"

st.set_page_config(page_title="Persistent AI Chat", layout="centered")
st.title("💾 Permanent Storage Chat Interface")
st.write("This app saves your conversations to a local JSON file so they persist even if you reload the dashboard.")
st.divider()

# =========================================================================
# 💾 PERSISTENCE HELPER FUNCTIONS
# =========================================================================
def load_stored_history():
    """Reads historical conversational arrays straight out of disk file storage."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history_to_disk(messages_list):
    """Saves operational context structures into a structural JSON data log."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages_list, f, indent=4)

# =========================================================================
# 🔄 MEMORY INITIALIZATION
# =========================================================================
if "messages" not in st.session_state:
    st.session_state.messages = load_stored_history()

# Render previous messages from the file cleanly on screen redraws
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =========================================================================
# 💬 CHAT UTILITY ENGINE RUN LOOP
# =========================================================================
if user_input := st.chat_input("Continue your conversation..."):
    
    # Display user input immediately
    with st.chat_message("user"):
        st.write(user_input)
        
    # Append new statement to the active array matrix
    st.session_state.messages.append({"role": "user", "content": user_input})
    save_history_to_disk(st.session_state.messages)  # Instantly write backup to disk
    
    # Generate model response window block container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            
            payload = {
                "model": MODEL_NAME,
                "messages": st.session_state.messages,
                "stream": False
            }
            
            try:
                response = requests.post(OLLAMA_CHAT_URL, json=payload)
                response.raise_for_status()
                
                result_data = response.json()
                ai_reply = result_data["message"]["content"].strip()
                
                # Render text output string
                st.write(ai_reply)
                
                # Append assistant's answer and save configuration array state to disk
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                save_history_to_disk(st.session_state.messages)
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Ensure your local Ollama desktop background app is open!")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

# Sidebar clear actions resetting file and runtime indices simultaneously
# FIXED: Modified styling type map assignment constraint
if st.sidebar.button("Wipe Permanent History File", type="primary"):
    st.session_state.messages = []
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    st.rerun()
