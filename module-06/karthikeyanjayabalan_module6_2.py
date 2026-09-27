# py -m streamlit run .\karthikeyanjayabalan_mod06_ex02_chatrag.py
# py -m pip install torchvision torch
# py -m streamlit run .\karthikeyanjayabalan_mod06_ex02_chatrag.py --server.fileWatcherType none




import os
import requests
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Configuration Settings
OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:latest"
# DOCUMENT_PATH = "sample.txt"
DOCUMENT_PATH = "MyRag.docx"

st.set_page_config(page_title="RAG Conversational Chat", layout="centered")
st.title("📚 Document-Grounded Chat RAG")
st.write("Ask questions about your documents. The assistant retrieves relevant context chunks using LangChain and Chroma.")
st.divider()

# =========================================================================
# 🔄 PHASE 1: BACKGROUND VECTOR DATABASE INITIALIZATION
# =========================================================================
@st.cache_resource
def initialize_vector_store():
    """Loads, splits, and embeds document chunks into a fast, cached Chroma vector instance."""
    if not os.path.exists(DOCUMENT_PATH):
        # Fallback safeguard file creation if missing
        with open(DOCUMENT_PATH, "w") as f:
            f.write("The office guidelines state that work hours are from 9 AM to 6 PM.\n"
                    "The main database uses SQLite for storage.\n"
                    "All Python exercises must follow strict variable naming conventions.\n")
            
    # loader = TextLoader(DOCUMENT_PATH)
    loader = Docx2txtLoader(DOCUMENT_PATH)
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(documents)
    
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma.from_documents(text_chunks, embeddings)
    return vector_db.as_retriever(search_kwargs={"k": 3})

# Load the document retriever engine
retriever = initialize_vector_store()

# =========================================================================
# 💾 PHASE 2: RUNTIME CONVERSATIONAL SESSION MEMORY
# =========================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages on screen layout re-renders
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# =========================================================================
# 💬 PHASE 3: INTERACTIVE CHAT EXECUTION
# =========================================================================
if user_input := st.chat_input("Ask a question about your documents..."):
    
    # Render user prompt choice instantly
    with st.chat_message("user"):
        st.write(user_input)
        
    # Append the raw question block to session logging state array
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Generate assistant text container window
    with st.chat_message("assistant"):
        with st.spinner("Retrieving document context and drafting response..."):
            
            try:
                # 1. RETRIEVAL STEP: Fetch the top 3 choices from our local database vector grid
                retrieved_docs = retriever.invoke(user_input)
                context_str = "\n".join([f"- {doc.page_content}" for doc in retrieved_docs])
                
                # 2. PROMPT ENRICHMENT STEP: Construct a system message instructing the LLM
                system_instruction = (
                    "You are a helpful office assistant. You must answer the user's question "
                    "using ONLY the following retrieved text blocks as factual source documents. "
                    "If the answer cannot be found in the context chunks, politely state that you do not know.\n\n"
                    f"Retrieved Reference Context:\n{context_str}"
                )
                
                # 3. CONTEXT INTEGRATION: Prepare the historical multi-turn message payload
                # We inject the temporary system instruction to ground the model's judgment
                api_messages = [{"role": "system", "content": system_instruction}] + st.session_state.messages
                
                payload = {
                    "model": MODEL_NAME,
                    "messages": api_messages,
                    "stream": False
                }
                
                # Dispatch the call to your local running Ollama instance
                response = requests.post(OLLAMA_CHAT_URL, json=payload)
                response.raise_for_status()
                
                result_data = response.json()
                ai_reply = result_data["message"]["content"].strip()
                
                # Render the final text answer on screen
                st.write(ai_reply)
                
                # Save answer back to history state array to keep dialogue coherent
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Ensure your local Ollama desktop background app is running!")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")

# Sidebar wipe action trigger clear button
if st.sidebar.button("Reset Chat Session", type="primary"):
    st.session_state.messages = []
    st.rerun()
