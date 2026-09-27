import streamlit as st
import requests
import json

st.title("🦙 Ollama AI Assistant")

# Use the Docker Compose service name 'ollama' as the hostname
OLLAMA_URL = "http://ollama:11434/api/generate"

# Input text box for the user
user_input = st.text_input("Ask the AI something:", placeholder="Type your prompt here...")

if st.button("Send") and user_input:
    with st.spinner("Thinking..."):
        try:
            # Payloads can target models like 'llama3', 'mistral', or 'phi3'
            payload = {
                "model": "llama3", 
                "prompt": user_input,
                "stream": False
            }
            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json().get("response", "No response received.")
                st.write("### AI Response:")
                st.info(result)
            else:
                st.error(f"Ollama returned an error status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to Ollama. Make sure the container is fully initialized and the model is downloaded.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
