from fastapi import FastAPI

from app.core.config import create_config

app = FastAPI(
     title="LoftBar",
     summary=(
          "Telegram Mini App for hookah bar orders"
     ),
     version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}