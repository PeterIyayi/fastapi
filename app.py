import os
import ssl
import time
import hmac
import hashlib
import certifi
import uvicorn
from typing import Dict
import langchain
from langchain_openai import ChatOpenAI

from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from slack_sdk import WebClient
from dotenv import load_dotenv
load_dotenv()
ssl_context = ssl.create_default_context(cafile=certifi.where())
SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
ngrok_token = os.environ.get("NGROK_AUTHTOKEN")
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"], ssl=ssl_context)

open_ai_token = os.environ["OPENAI_API_KEY"]

app = FastAPI()

def verify_slack_request(signing_secret: str, body: bytes, timestamp: str, slack_signature: str) -> bool:

    basestring = f"v0:{timestamp}:{body.decode('utf-8')}".encode('utf-8')
    computed = 'v0=' + hmac.new(signing_secret.encode('utf-8'), basestring, hashlib.sha256).hexdigest()
    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(computed, slack_signature)



@app.post("/slack/events")
async def slack_events(request: Request):
    payload = await request.json()

    # Handle URL verification challenge
    if payload.get("type") == "url_verification":
        return {"challenge": payload.get("challenge")}

    # Ignore retries from Slack
    if "X-Slack-Retry-Num" in request.headers:
        return {"ok": True}

    # Handle event callbacks
    if payload.get("type") == "event_callback":
        event = payload.get("event", {})

        # Ignore messages from bots (including this bot)
        if event.get("subtype") == "bot_message" or event.get("bot_id"):
            return {"ok": True}

        # Only handle plain user messages
        if event.get("type") == "message" and event.get("subtype") is None:
            channel = event.get("channel")
            user = event.get("user")
            text = event.get("text", "")
            ts = event.get("ts")

            print(f"Message from {user} in {channel} at {ts}: {text}")

            # Example: generate AI response
            ai_response = await call_my_ai(text)  # your AI function here

            # Send the AI response back
            await send_message(channel, ai_response)

            return {"ok": True}

    return {"ok": True}


async def send_message(channel: str, text: str):
    # Simple wrapper using slack_sdk WebClient
    resp = client.chat_postMessage(channel=channel, text=text)
    return resp

async def call_my_ai(user_input:str) -> str:
    llm = ChatOpenAI(model="gpt-4.1-nano")
    llm_response = llm.invoke(user_input)
    response = llm_response.content
    return response




# if __name__ == "__main__":
    uvicorn.run(
        "app:app",        # <module>:<FastAPI instance name>
        host="0.0.0.0",
        port=8000,
        reload=True       # auto-reloads on code changes
    )