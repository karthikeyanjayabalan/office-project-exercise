import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_pirate_llm(model_name="llama3.2:latest"):
    print(f"--- Local LLM Personality Engine ({model_name}) ---")
    print("The AI is currently configured with a Pirate Captain persona.")
    print("Type 'quit' to exit the active chat layout.\n")
    
    # Foundational directives locked across the session
    SYSTEM_INSTRUCTION = (
        "You are a gruff, salty Pirate Captain sailing the digital high seas. "
        "You must answer all user questions using pirate slang, sea jargon, "
        "and start or end your sentences with phrases like 'Ahoy!', 'Matey!', or 'Shiver me timbers!'."
    )
    
    while True:
        user_prompt = input("You: ").strip()
        
        if user_prompt.lower() in ["quit", "exit"]:
            print("Lowering sails. Goodbye, matey!")
            break
            
        if not user_prompt:
            continue
            
        full_context_prompt = f"System Instruction: {SYSTEM_INSTRUCTION}\n\nUser Question: {user_prompt}"
        
        payload = {
            "model": model_name,
            "prompt": full_context_prompt,
            "stream": False
        }
        
        print("Captain is drafting a response...", end="\r")
        
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            
            result_data = response.json()
            ai_response = result_data.get("response", "").strip()
            
            # Wipe loading characters cleanly
            print(" " * 40, end="\r")
            
            print(f"Pirate AI: {ai_response}\n")
            print("-" * 60)
            
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")
            break

if __name__ == "__main__":
    ask_pirate_llm()
