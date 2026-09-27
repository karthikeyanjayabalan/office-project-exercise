import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def ask_local_llm(model_name="llama3.2:latest"):
    print(f"--- Local LLM Chat Interface Engine ({model_name}) ---")
    print("Type 'quit' or 'exit' to stop the program.\n")
    
    while True:
        user_prompt = input("You: ").strip()
        
        if user_prompt.lower() in ["quit", "exit"]:
            print("Closing LLM API session. Goodbye!")
            break
            
        if not user_prompt:
            continue
            
        payload = {
            "model": model_name,
            "prompt": user_prompt,
            "stream": False
        }
        
        # We print the thinking prompt statement
        print("AI is thinking...", end="\r")
        
        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            
            result_data = response.json()
            ai_response = result_data.get("response", "").strip()
            
            # 🆕 THE FIX: We print empty spaces to completely wipe out the "AI is thinking..." characters first
            print(" " * 30, end="\r")
            
            print(f"AI: {ai_response}\n")
            print("-" * 50)
            
        except Exception as e:
            print(f"\nAn error occurred: {e}\n")
            break

if __name__ == "__main__":
    ask_local_llm()



# import json
# import requests

# # The local endpoint url automatically hosted by Ollama
# OLLAMA_URL = "http://localhost:11434/api/generate"

# def ask_local_llm(model_name="llama3.2"):
#     print(f"--- Local LLM Chat Interface Engine ({model_name}) ---")
#     print("Type 'quit' or 'exit' to stop the program.\n")
    
#     while True:
#         # 1. Capture dynamic text input from the user
#         user_prompt = input("You: ").strip()
        
#         if user_prompt.lower() in ["quit", "exit"]:
#             print("Closing LLM API session. Goodbye!")
#             break
            
#         if not user_prompt:
#             continue
            
#         # 2. Structure the payload parameter map for the Ollama API
#         payload = {
#             "model": model_name,
#             "prompt": user_prompt,
#             "stream": False  # Set to False to get the entire answer block at once
#         }
        
#         print("AI is thinking...", end="\r")
        
#         try:
#             # 3. Send the request to your local running Ollama instance
#             response = requests.post(OLLAMA_URL, json=payload)
#             response.raise_for_status()
            
#             # 4. Extract and display the generated response text field
#             result_data = response.json()
#             ai_response = result_data.get("response", "").strip()
            
#             print(f"AI: {ai_response}\n")
#             print("-" * 50)
            
#         except requests.exceptions.ConnectionError:
#             print("\nError: Could not connect to Ollama server.")
#             print("Make sure Ollama is open and running in your background taskbar or terminal!\n")
#             break
#         except Exception as e:
#             print(f"\nAn error occurred while processing the request: {e}\n")

# if __name__ == "__main__":
#     # 📌 NOTE: If you downloaded a different model (like 'phi3' or 'qwen2.5'), 
#     # change the string parameter below to match your downloaded model name!
#     # ask_local_llm("llama3.2")
#     ask_local_llm("llama3.2:latest")

