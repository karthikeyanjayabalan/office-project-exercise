#py -m streamlit run .\karthikeyanjayabalan_mod05_ex06_chat.py

import streamlit as st
import requests

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:latest"

st.set_page_config(page_title="Conversational AI Chat", layout="centered")
st.title("💬 State-Aware Conversational Chat")
st.write("This interface preserves chat history across multiple turns using `st.session_state`.")
st.divider()

# 1. INITIALIZE CHAT MEMORY SCHEMA: Create the history list if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. RENDER THE CHAT HISTORY: Display previous messages cleanly on screen redraws
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 3. CAPTURE NEW INPUT: Render a native chat entry bar at the bottom
if user_input := st.chat_input("Message your local AI..."):
    
    # Display what the user typed instantly
    with st.chat_message("user"):
        st.write(user_input)
        
    # Append the user's message to our in-memory session tracking state list
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Process the model response container window block
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            
            # 📌 CONTEXT INJECTION: We pass the entire message history array to the server
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
                
                # Render the final text string onto the canvas container block
                st.write(ai_reply)
                
                # Save the assistant's reply into history so memory continues to scale
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Ensure your local Ollama desktop background app is open!")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

# Sidebar reset clear action trigger button utility
if st.sidebar.button("Clear Chat History", type="secondary"):
    st.session_state.messages = []
    st.rerun()
