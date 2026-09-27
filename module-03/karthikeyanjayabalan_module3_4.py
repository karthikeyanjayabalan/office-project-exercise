import random
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Karthik's_Module03_Exercise04_BackAndForth")
MEMORY_DB = []

class Person(BaseModel):
    name: str
    phone_number: str

@app.post("/person")
def create_person(person: Person):
    MEMORY_DB.clear()
    MEMORY_DB.append(person.dict())
    return {"message": "Person recorded successfully", "data": person}

@app.get("/person")
def get_and_modify_person():
    if not MEMORY_DB:
        raise HTTPException(status_code=404, detail="No data available in server memory session.")
    
    person_info = MEMORY_DB[0].copy()
    # Generate a random tracking ID parameter and merge it into the payload
    person_info["random_id"] = random.randint(1000, 9999)
    
    return {
        "title": "--- Retrieved & Updated Person Data ---",
        "name": person_info["name"],
        "phone_number": person_info["phone_number"],
        "random_id": person_info["random_id"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9004)
