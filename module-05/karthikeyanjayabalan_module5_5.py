
"""
What is Temperature?Temperature is a value (usually between 0.0 and 1.5) that controls the 
randomness or creativity of an LLM's responses:Low Temperature (0.0 - 0.2): Highly predictable, factual, and repetitive. 
The model always picks the most mathematically probable next token. 
Excellent for coding and math.High Temperature (0.7 - 1.2): Creative, diverse, and random. The model explores lower-probability tokens. 
Great for storytelling or brainstorming, but prone to hallucinations.
"""

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_configured_llm(model_name="llama3.2:latest"):
    print(f"--- Local LLM Configuration Engine ({model_name}) ---")
    print("Configured Parameters: Context Window = 8192 tokens | Temperature = 1.2")
    print("Type 'quit' to exit the current session.\n")
    
    while True:
        user_prompt = input("You: ").strip()
        
        if user_prompt.lower() in ["quit", "exit"]:
            print("Closing session. Goodbye!")
            break
            
        if not user_prompt:
            continue
            
        # 📌 OPTIONS BLOCK: Dynamically sets temperature and context limits on the server
        payload = {
            "model": model_name,
            "prompt": user_prompt,
            "stream": False,
            "options": {
                "temperature": 1.2,    # High creativity / randomness setting
                "num_ctx": 8192        # Expands memory window tracking limit
            }
        }
        
        print("Processing with custom configurations...", end="\r")
        
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            
            result_data = response.json()
            ai_response = result_data.get("response", "").strip()
            
            # Wipe terminal loading lines cleanly
            print(" " * 45, end="\r")
            
            print(f"AI: {ai_response}\n")
            print("-" * 60)
            
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")
            break

if __name__ == "__main__":
    ask_configured_llm()
