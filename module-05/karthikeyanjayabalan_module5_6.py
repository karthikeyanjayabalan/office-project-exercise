#py -m streamlit run .\karthikeyanjayabalan_mod05_ex06_chat.py


import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

# 1. Configure Web Browser Tab Title and Sidebar Layout
st.set_page_config(page_title="Local LLM Chat Interface", layout="centered")

st.title("🤖 Local LLM Web Interface")
st.write(f"Powered by Ollama Module Server (`{MODEL_NAME}`)")
st.divider()

# 2. Render Text Box Input Panel for user questions
user_question = st.text_input("Ask your local AI a question:", placeholder="Type here (e.g., What is 104 power 3?)...")

# 3. Handle Form Execution Submission
if st.button("Submit Question", type="primary"):
    if user_question.strip() == "":
        st.warning("Please type a valid question before submitting.")
    else:
        # Create a visual spinning loading wheel component while waiting for HTTP response
        with st.spinner("AI engine is processing your request..."):
            payload = {
                "model": MODEL_NAME,
                "prompt": user_question.strip(),
                "stream": False
            }
            
            try:
                # Dispatch POST API call to background Ollama instance
                response = requests.post(OLLAMA_URL, json=payload)
                response.raise_for_status()
                
                result_data = response.json()
                ai_response = result_data.get("response", "").strip()
                
                # Render clean layout containers showing the output response
                st.subheader("💡 AI Response:")
                st.info(ai_response)
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Failed: Could not connect to your local Ollama server. Ensure the desktop application is running in the background!")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
