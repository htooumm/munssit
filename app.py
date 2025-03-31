import os
from fastapi import FastAPI, Request, HTTPException
from src.whatsapp_integration import process_webhook
from src.rag_implementation import query_menu
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# إنشاء تطبيق FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Restaurant WhatsApp Bot API is running!"}

@app.get("/webhook")
async def verify_webhook(request: Request):
    # التحقق من Webhook (مطلوب لـ WhatsApp)
    params = dict(request.query_params)
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == os.getenv("VERIFY_TOKEN", "your_verification_token_here"):
        return int(params.get("hub.challenge", 0))
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def webhook(request: Request):
    # معالجة رسائل WhatsApp الواردة
    body = await request.json()
    return await process_webhook(body)

@app.get("/test")
async def test_rag(query: str = "ما هي أنواع الشاورما لديكم؟"):
    # اختبار نظام RAG
    response = query_menu(query)
    return {"query": query, "response": response}

# تشغيل التطبيق إذا تم تنفيذه مباشرة
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("app:app", host=host, port=port, reload=True)
