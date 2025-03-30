from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from src.config import WEBHOOK_PATH, VERIFY_TOKEN, APP_PORT, APP_HOST
from src.vector_store import init_pinecone
from src.ai_handler import GeminiAI
from src.whatsapp_handler import WhatsAppHandler

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Restaurant WhatsApp Bot")

# Initialize Pinecone
pinecone_index = init_pinecone()

# Initialize AI handler
ai_handler = GeminiAI(pinecone_index)

# Initialize WhatsApp handler
whatsapp_handler = WhatsAppHandler(ai_handler)

@app.get("/")
async def root():
    return {"status": "active", "message": "Restaurant WhatsApp Bot is running"}

@app.get(WEBHOOK_PATH)
async def verify_webhook(request: Request):
    """
    Verify webhook for WhatsApp API
    """
    # Get query parameters
    query_params = dict(request.query_params)
    
    # Check if verification token is correct
    if query_params.get("hub.verify_token") == VERIFY_TOKEN:
        # Return challenge
        return int(query_params.get("hub.challenge", 0))
    
    # Return error if token is invalid
    raise HTTPException(status_code=403, detail="Verification token mismatch")

@app.post(WEBHOOK_PATH)
async def webhook(request: Request):
    """
    Handle incoming webhook events from WhatsApp
    """
    try:
        # Get request body
        body = await request.json()
        
        # Handle message
        result = whatsapp_handler.handle_message(body)
        
        return JSONResponse(content=result)
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return JSONResponse(content={"status": "error", "message": str(e)})

def start():
    """Start the FastAPI server"""
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)

if __name__ == "__main__":
    start()
