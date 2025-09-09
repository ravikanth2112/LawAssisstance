from fastapi import FastAPI

from app.api.v1.users import router as users_router
from app.core.config import settings

app = FastAPI(title="LawAssistance API", version="0.1.0")

app.include_router(users_router, prefix="/api/v1")


@app.get("/healthz", tags=["health"])
def health() -> dict:
    return {"status": "ok"}
