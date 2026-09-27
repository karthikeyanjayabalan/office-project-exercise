# npx @modelcontextprotocol/inspector py karthikeyanjayabalan_mod08_ex01_mcp.py 
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process


import datetime
import random
from fastmcp import FastMCP

# Initialize a clean FastMCP server instance
mcp = FastMCP("System Info Server")

# 🛠️ TOOL 1: Fetching current system date
@mcp.tool()
def get_system_date() -> str:
    """Returns the current local system date string from the server."""
    now = datetime.datetime.now()
    return f"Current System Date: {now.strftime('%Y-%m-%d %H:%M:%S')}"

# 🛠️ TOOL 2: Generating random numbers
@mcp.tool()
def generate_random_number(min_val: int = 1000, max_val: int = 9999) -> str:
    """Generates a random tracking identifier or integer value within specified constraints."""
    num = random.randint(min_val, max_val)
    return f"Generated Tracking Identifier: {num}"

if __name__ == "__main__":
    # Start the fastmcp protocol engine process loop
    mcp.run()
