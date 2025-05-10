# backend/app/routes/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
import json
import os

chat_router = APIRouter()

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'health_knowledge.json')

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

def load_data():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def match_symptom(message, data):
    matched = []
    for item in data:
        for symptom in item["trieu_chung"]:
            if symptom.lower() in message.lower():
                matched.append(item)
                break
    return matched

@chat_router.post("/", response_model=ChatResponse)
def handle_chat(req: ChatRequest):
    data = load_data()
    matched_data = match_symptom(req.message, data)

    if not matched_data:
        return {"reply": "Xin lỗi, tôi chưa có đủ dữ liệu để tư vấn cho triệu chứng này. Vui lòng miêu tả rõ hơn hoặc thử lại sau."}

    reply_parts = []
    for item in matched_data:
        reply = f"""
Phân tích triệu chứng:
- Nguyên nhân có thể: {", ".join(item["nguyen_nhan"])}
- Giải pháp gợi ý: {", ".join(item["giai_phap"])}
- Cảnh báo: {item["canh_bao"]}
"""
        reply_parts.append(reply.strip())

    return {"reply": "\n\n---\n\n".join(reply_parts)}
