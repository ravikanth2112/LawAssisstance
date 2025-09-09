from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import uuid

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

users_db = {
    "lawyer@test.com": {"id": "lawyer-1", "first_name": "John", "last_name": "Lawyer", "email": "lawyer@test.com", "password": "test123", "user_type": "lawyer"},
    "client@test.com": {"id": "client-1", "first_name": "Jane", "last_name": "Client", "email": "client@test.com", "password": "test123", "user_type": "client"}
}

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def root():
    return {"message": "Test Auth API", "users": len(users_db)}

@app.post("/api/auth/login")
def login(data: LoginRequest):
    print(f"Login attempt: {data.email}")
    user = users_db.get(data.email)
    if not user or user["password"] != data.password:
        raise HTTPException(401, "Invalid email or password")
    return {"access_token": f"test-token-{user[\"id\"]}", "user": user}

@app.post("/api/auth/register")  
def register(data: dict):
    if data["email"] in users_db:
        raise HTTPException(400, "User already exists")
    user_id = str(uuid.uuid4())
    user = {"id": user_id, **data}
    users_db[data["email"]] = user
    return {"access_token": f"test-token-{user_id}", "user": user}

print("Starting Test Auth Server on http://127.0.0.1:8001")
uvicorn.run(app, host="127.0.0.1", port=8001)
