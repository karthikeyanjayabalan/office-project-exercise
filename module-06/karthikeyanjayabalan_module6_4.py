# py -m pip install langchain-ollama langchain-core


import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

# 1. DEFINE THE MATHEMATICAL TOOL [4]
def calculate_math_expression(expression: str) -> str:
    """Useful for when you need to calculate mathematical expressions or basic arithmetic operations."""
    try:
        # Format the math expression string to be valid Python math syntax (e.g. 104^3 -> 104**3)
        clean_expr = expression.replace("^", "**")
        allowed_names = {"__builtins__": None}
        result = eval(clean_expr, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error executing calculation: {str(e)}."

def run_math_agent(user_query: str):
    print(f"--- Starting ReAct Execution Loop ---")
    print(f"Target Request: '{user_query}'\n")

    # 2. CONSTRUCT THE RE-ACT REASONING PROMPT TEMPLATE [4]
    template = """You are a helpful mathematical assistant. You have access to the following tool:

Tool Name: calculate_math_expression
Description: Useful for calculating math expressions or arithmetic. Input must be a raw math string like 104**3 or 5+5.

To use a tool, you MUST use the exact format:
Thought: Do I need to use a tool? Yes
Action: calculate_math_expression
Action Input: [your math expression here]

When you have the final answer, or do not need a tool, you MUST use the format:
Thought: Do I need to use a tool? No
Final Answer: [your final numerical response here]

Question: {input}
"""
    full_prompt = template.format(input=user_query)
    
    print("Agent is reasoning... (Step 1: Thought Process)")
    
    # 3. DISPATCH INITIAL THOUGHT STEP TO OLLAMA
    try:
        payload = {"model": MODEL_NAME, "prompt": full_prompt, "stream": False}
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        ai_thought = response.json().get("response", "")
        
        print("\n=======================================================")
        print(" AGENT REASONING STEP")
        print("=======================================================")
        print(ai_thought.strip())
        
        # 4. PARSE FOR TOOL INVOCATION SIGNALS
        if "Action Input:" in ai_thought:
            # Extract the raw math equation inside the action input text string
            math_expr = ai_thought.split("Action Input:")[-1].strip()
            # Clean up trailing formatting characters if present
            math_expr = re.sub(r'[^0-9\+\-\*\/\(\)\^]', '', math_expr)
            
            print(f"\n[Tool Execution] Calling calculate_math_expression with: '{math_expr}'")
            # Run our Python math tool function
            tool_observation = calculate_math_expression(math_expr)
            print(f"[Tool Observation] Result returned: {tool_observation}")
            
            # Feed the observation back to the model for the final confirmation loop
            final_prompt = full_prompt + f"\n{ai_thought}\nObservation: {tool_observation}\nThought: Do I need to use a tool? No\nFinal Answer:"
            
            payload = {"model": MODEL_NAME, "prompt": final_prompt, "stream": False}
            response = requests.post(OLLAMA_URL, json=payload)
            ai_final = response.json().get("response", "")
            
            print(f"\n=======================================================")
            print(f" AGENT FINAL RESPONSE")
            print(f"=======================================================")
            print(f"The answer is {tool_observation}. {ai_final.strip()}")
            print(f"=======================================================\n")
        else:
            # If the model directly answered without needing a tool call
            print(f"\n=======================================================")
            print(f" AGENT FINAL RESPONSE")
            print(f"=======================================================")
            print(ai_thought.strip())
            print(f"=======================================================\n")
            
    except Exception as e:
        print(f"\n❌ RUNTIME ERROR OCCURRED: {e}\n")

if __name__ == "__main__":
    run_math_agent("What is 2^2 + 5*5?")

