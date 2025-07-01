import os
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World from Railway!"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting test server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 