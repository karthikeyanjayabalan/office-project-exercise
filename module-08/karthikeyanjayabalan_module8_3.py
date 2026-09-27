# npx @modelcontextprotocol/inspector py karthikeyanjayabalan_mod08_ex03_mcpollama.py


import requests
from fastmcp import FastMCP

# Initialize an MCP server instance optimized for handling local model queries
mcp = FastMCP("Ollama Protocol Server")

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

# 🛠️ MCP TOOL: Connecting user questions directly to local Ollama endpoints
@mcp.tool()
def ask_local_language_model(question: str) -> str:
    """Useful for answering general knowledge questions, debugging code, or analyzing text using the local LLM engine."""
    payload = {
        "model": MODEL_NAME,
        "prompt": question.strip(),
        "stream": False
    }
    
    try:
        # Dispatch the request block to your active local Ollama instance
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        
        result_data = response.json()
        return result_data.get("response", "").strip()
        
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the local Ollama server instance. Make sure the Ollama desktop app is open and running in your taskbar background!"
    except Exception as e:
        return f"An error occurred while processing the model transaction: {e}"

if __name__ == "__main__":
    mcp.run()
