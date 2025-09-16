import os
import time
import hmac
import hashlib
import uvicorn
from typing import Dict
import langchain
from langchain_openai import ChatOpenAI

from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
from slack_sdk import WebClient
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(model="gpt-4.1-nano")
llm_response = llm.invoke("hello")
print(llm_response.content)