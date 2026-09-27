import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Karthik's_Module03_Exercise03_TypeCorrectly")

class TextPayload(BaseModel):
    text: str  # Mandatory field. If missing, FastAPI auto-rejects with a 422 error status code.

@app.post("/check-text")
def check_text(payload: TextPayload):
    return {"status": "Valid", "received_text": payload.text}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9003)
