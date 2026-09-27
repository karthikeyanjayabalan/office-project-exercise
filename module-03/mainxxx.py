"""
module03-exercise01
====================
make python code using fast API to return a message with person name (/hello?name = Mohamed ) 
- >{"message": "Hello Mohamed"
"""

from importlib import import_module

# Initialize the FastAPI application
FastAPI = import_module("fastapi").FastAPI
app = FastAPI()


@app.get("/hello")
def say_hello(name: str):
    """Returns a personalized greeting message via a query parameter."""
    return {"message": f"Hello {name}, welcome to FastAPI!"}
