# py -m streamlit run .\karthikeyanjayabalan_module06_exercise06_structure.py --server.fileWatcherType none

import sqlite3
import json
import requests
import streamlit as st
from pydantic import BaseModel, Field
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"
DB_NAME = "structured_userdata.db"

st.set_page_config(page_title="Pydantic Structure UI", layout="centered")
st.title("📋 Pydantic Structured Data Extractor")
st.write("Enter text details. The LLM extracts data parameters into a validated Pydantic layout before archiving to SQLite.")
st.divider()

# =========================================================================
# 🏗️ PHASE 1: PYDANTIC SCHEMA DEFINITION
# =========================================================================
class UserInformation(BaseModel):
    name: Optional[str] = Field(default=None, description="The extracted name of the individual person.")
    time: Optional[str] = Field(default=None, description="The extracted clock time or date instance description.")
    number: Optional[str] = Field(default=None, description="The extracted phone tracking identifier or numerical string value.")

# =========================================================================
# 🔄 PHASE 2: DATABASE BACKEND STORAGE SETUP
# =========================================================================
def init_structured_database():
    """Initializes the structured data tracking table inside SQLite if missing."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS structured_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        extracted_name TEXT,
        extracted_time TEXT,
        extracted_number TEXT,
        logged_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def save_pydantic_to_db(profile: UserInformation):
    """Saves the validated parameters of a Pydantic model directly to SQLite rows."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO structured_profiles (extracted_name, extracted_time, extracted_number) VALUES (?, ?, ?);",
        (profile.name, profile.time, profile.number)
    )
    conn.commit()
    conn.close()

# Initialize the profile schema database on launch
init_structured_database()

# =========================================================================
# 💬 PHASE 3: INTERACTIVE SCREEN WEB RUNTIME GRAPHICS
# =========================================================================
user_paragraph = st.text_area(
    "Enter raw statement or scenario paragraph describing a person:",
    placeholder="Example: My friend Mohamed called me at 3 PM from his number 0501234567..."
)

if st.button("Extract & Validate Schema", type="primary"):
    if user_paragraph.strip() == "":
        st.warning("Please input descriptive text guidelines first.")
    else:
        with st.spinner("LLM is parsing parameters into JSON structure..."):
            
            extraction_prompt = f"""You are a data extraction bot. Your job is to read the text below and extract information into a JSON object matching this exact scheme:
{{
  "name": "extracted name string or null",
  "time": "extracted time string or null",
  "number": "extracted numerical string or null"
}}

Rules:
- Output ONLY valid JSON code block markup syntax. 
- Do NOT include conversational explanations.
- If a parameter value cannot be found, set it to null.

Text to analyze:
"{user_paragraph.strip()}"
"""
            payload = {
                "model": MODEL_NAME,
                "prompt": extraction_prompt,
                "stream": False,
                "format": "json" # Forces Ollama to output valid JSON text strings
            }
            
            try:
                response = requests.post(OLLAMA_URL, json=payload)
                response.raise_for_status()
                
                raw_json_str = response.json().get("response", "").strip()
                
                #  FIXED: Using json.loads() safely interprets 'null' values into Python 'None' objects
                parsed_dict = json.loads(raw_json_str)
                
                # Feed the dictionary into Pydantic to ensure type safety conformance
                validated_profile = UserInformation(**parsed_dict)
                
                # ENFORCEMENT CHECK: Ensure at least one element parameter is present
                if not validated_profile.name and not validated_profile.time and not validated_profile.number:
                    st.error("❌ Schema Validation Error: At least one informational field (name, time, or number) must be given by the user!")
                else:
                    # STORAGE STEP: Save the safe Pydantic instance into SQLite database
                    save_pydantic_to_db(validated_profile)
                    
                    st.subheader("💡 Validated Output Matrix Framework:")
                    st.json(validated_profile.dict())
                    st.success("✅ Pydantic data model schema validated and saved into 'structured_userdata.db' successfully!")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Connection Error: Ensure your local Ollama desktop background app is open!")
            except Exception as e:
                st.error(f"❌ Structural Extraction Failed. Details: {e}")

# =========================================================================
# 📊 PHASE 4: SIDEBAR HISTORY LOG PREVIEW
# =========================================================================
st.sidebar.header("📜 Structured SQLite Records")
if st.sidebar.button("Refresh Table Records", type="secondary"):
    st.rerun()

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, extracted_name, extracted_time, extracted_number, datetime(logged_at, '+4 hours') FROM structured_profiles ORDER BY id DESC LIMIT 5;")
    saved_rows = cursor.fetchall()
    conn.close()
    
    if not saved_rows:
        st.sidebar.info("No records present in DB yet.")
    else:
        for row in saved_rows:
            st.sidebar.markdown(f"**Record ID: {row[0]}** | *{row[4]}*")
            st.sidebar.markdown(f"👤 Name: `{row[1]}`")
            st.sidebar.markdown(f"⏰ Time: `{row[2]}`")
            st.sidebar.markdown(f"🔢 Number: `{row[3]}`")
            st.sidebar.divider()
except Exception:
    st.sidebar.error("Could not fetch structured profiles.")

