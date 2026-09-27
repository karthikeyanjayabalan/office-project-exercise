import json
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:latest"

# 🛠️ THE MATHEMATICAL TOOL USED BY AGENT 1
def calculate_math_expression(expression: str) -> str:
    """Safely executes basic arithmetic calculations in an isolated dictionary scope."""
    try:
        clean_expr = expression.replace("^", "**")
        allowed_names = {"__builtins__": None}
        result = eval(clean_expr, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error executing calculation: {str(e)}."

def run_multi_agent_system(user_query: str):
    print(f"=======================================================")
    print(f" INITIALIZING MULTI-AGENT COLLABORATION PIPELINE")
    print(f"=======================================================\n")
    print(f"User Request: '{user_query}'\n")

    # -------------------------------------------------------------------------
    # 🤖 AGENT 1: THE CALCULATOR AGENT
    # -------------------------------------------------------------------------
    print("🤖 [Agent 1: Calculator] Analyzing query and executing math tool...")
    
    react_template = """You are a precise mathematical tool-use assistant.
Tool Name: calculate_math_expression
Description: Computes equations. Input must be a raw math string like 104**3.

You MUST use the exact format:
Thought: Do I need to use a tool? Yes
Action: calculate_math_expression
Action Input: [your math expression here]

Question: {input}
"""
    try:
        payload = {"model": MODEL_NAME, "prompt": react_template.format(input=user_query), "stream": False}
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        agent1_thought = response.json().get("response", "")
        
        calculated_result = "Could not parse computation."
        
        if "Action Input:" in agent1_thought:
            math_expr = agent1_thought.split("Action Input:")[-1].strip()
            math_expr = re.sub(r'[^0-9\+\-\*\/\(\)\^]', '', math_expr)
            
            # Execute the calculation tool
            calculated_result = calculate_math_expression(math_expr)
            print(f"   ↳ Tool Call Executed: '{math_expr}' ➜ Result: {calculated_result}")
        else:
            print("   ↳ Agent 1 did not invoke the calculation tool.")
            
        print("✔ Agent 1 execution complete.\n" + "-"*60)

        # -------------------------------------------------------------------------
        # 🤖 AGENT 2: THE REFLECTION & CRITIQUE AGENT
        # -------------------------------------------------------------------------
        print("🤖 [Agent 2: Reflection Agent] Intercepting output and reflecting...")
        
        reflection_prompt = f"""You are a senior quality assurance and reflection agent. 
Your job is to review the mathematical work performed by Agent 1 and provide a structured reflection.

Original User Question: {user_query}
Agent 1 Computation Result: {calculated_result}

Please output your reflection using this exact structural layout:
1. VERIFICATION STATUS: [State if the calculation matches the mathematical question intent (Passed/Failed)]
2. STEP-BY-STEP BREAKDOWN: [Explain the logical arithmetic steps behind the answer]
3. FINAL CONCLUSION: [Provide a professional summary sentence of the result]
"""
        payload = {"model": MODEL_NAME, "prompt": reflection_prompt, "stream": False}
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        agent2_reflection = response.json().get("response", "")
        
        print("\n=======================================================")
        print(" AGENT 2: FINAL REFLECTION REPORT")
        print("=======================================================")
        print(agent2_reflection.strip())
        print(f"=======================================================\n")
        
    except Exception as e:
        print(f"\n❌ MULTI-AGENT EXECUTION ERROR: {e}\n")

if __name__ == "__main__":
    # Test case matching your previous parameters
    run_multi_agent_system("Calculate (45 + 55) * (20 - 15)")
