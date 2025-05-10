# backend/app/main.py
from fastapi import FastAPI
from app.routes.chat import chat_router

app = FastAPI(
    title="AI Tư Vấn Sức Khỏe",
    description="API xử lý tư vấn sức khỏe người dùng bằng AI",
    version="1.0"
)

app.include_router(chat_router, prefix="/chat")
