import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Karthik's_Module03_Exercise01_HelloAPI")

@app.get("/hello")
def say_hello(name: str = "User"):
    # Returns a json message mapping back to the query input parameter
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9001)
