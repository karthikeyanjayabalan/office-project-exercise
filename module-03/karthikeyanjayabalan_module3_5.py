import logging
import uvicorn
from fastapi import FastAPI, Request

# Configure structural logging targets simultaneously
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("my_file.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI(title="Karthik's_Module03_Exercise05_Logging")

@app.middleware("http")
async def process_logging_middleware(request: Request, call_next):
    response = await call_next(request)
    # Extract structural route indicators per assignment rules
    log_line = f"Method: {request.method} | Path: {request.url.path} | Status: {response.status_code}"
    logging.info(log_line)
    return response

@app.get("/test-log")
def test_log_endpoint():
    return {"status": "Logger executed successfully."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9005)
