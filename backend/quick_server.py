from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

users_db = {}

@app.get("/")
def root():
    return {"message": "Backend is running", "users": len(users_db)}

@app.get("/health") 
def health():
    return {"status": "OK", "message": "Server healthy"}

print("Starting server on http://127.0.0.1:8000")
uvicorn.run(app, host="127.0.0.1", port=8000)

