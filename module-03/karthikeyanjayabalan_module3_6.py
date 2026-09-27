from math import ceil
import uvicorn
from fastapi import FastAPI, Query

app = FastAPI(title="Karthik's_Module03_Exercise06_Pagination")

# Seed an internal mock data list of 25 items to demonstrate boundaries
MOCK_DATA = [{"id": i, "name": f"Office Item #{i}"} for i in range(1, 101)]

@app.get("/items")
def get_paginated_items(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=5, ge=1)
):
    total_items = len(MOCK_DATA)
    total_pages = ceil(total_items / size)
    
    start_idx = (page - 1) * size
    end_idx = start_idx + size
    sliced_data = MOCK_DATA[start_idx:end_idx]
    
    return {
        "metadata": {
            "total_items": total_items,
            "current_page": page,
            "per_page": size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        },
        "items": sliced_data
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9006)
