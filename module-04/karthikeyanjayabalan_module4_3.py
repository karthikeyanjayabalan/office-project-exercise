import sqlite3
import random
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Module 04 - Exercise 03: Person API")
DB_NAME = "office_tasks.db"

class PersonCreate(BaseModel):
    name: str
    phone_number: str

# 🆕 AUTOMATED TABLE INITIALIZER: Creates the table automatically on startup if missing
@app.on_event("startup")
def verify_or_create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        random_id INTEGER,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()
    print("--- [Startup] 'people' database table verification complete ---")

# 1. POST ENDPOINT: Accepts a List of PersonCreate items
@app.post("/person")
def create_people(people: List[PersonCreate]):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        saved_records = []
        
        for person in people:
            generated_random_id = random.randint(1000, 9999)
            
            cursor.execute(
                "INSERT INTO people (name, phone_number, random_id) VALUES (?, ?, ?);",
                (person.name, person.phone_number, generated_random_id)
            )
            
            saved_records.append({
                "database_id": cursor.lastrowid,
                "name": person.name,
                "phone_number": person.phone_number,
                "random_id": generated_random_id
            })
            
        conn.commit()
        
        return {
            "message": f"Successfully inserted {len(saved_records)} person record(s) into database!",
            "inserted_count": len(saved_records),
            "records": saved_records
        }
        
    except sqlite3.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Database operational failure: {e}")
    finally:
        conn.close()

# 2. GET ENDPOINT: Fetches all entries over HTTP
@app.get("/person")
def get_all_people():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, phone_number, random_id, datetime(created_at, '+4 hours') FROM people;")
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "db_id": row[0],
                "name": row[1],
                "phone_number": row[2],
                "random_id": row[3],
                "local_created_at": row[4]
            })
        return {"total_records": len(results), "people": results}
    finally:
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8005)
