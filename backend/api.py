from fastapi import FastAPI,HTTPException,Depends,Request,Header,status
from pydantic import BaseModel
from typing import List,Optional
#from ai.olama import OllamaAPI
import uvicorn
import hmac
import hashlib
import json
import os
import time
from dotenv import load_dotenv

import asyncio
import atexit
import warnings
import sys
from openai import OpenAI
import requests
import aiohttp
import asyncio
from typing import Optional
import json



load_dotenv()

async def ask_chat_gpt_async(request: str, session: aiohttp.ClientSession) -> str:
    url = "https://openrouter.ai/api/v1/responses"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPEN_AI')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-5-nano",
        "input": request
    }
    
    try:
        async with session.post(url, headers=headers, json=payload, timeout=30) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('output_text', '')
            else:
                # Логирование ошибки
                return f"Ошибка API: {response.status}"
    except asyncio.TimeoutError:
        return "Таймаут запроса"
    except Exception as e:
        return f"Ошибка: {str(e)}"



warnings.filterwarnings("ignore", category=RuntimeWarning)


original_excepthook = sys.excepthook
def custom_excepthook(type, value, traceback):
    if type == RuntimeError and "Event loop is closed" in str(value):
        return
    original_excepthook(type, value, traceback)

sys.excepthook = custom_excepthook





 


client = OpenAI(api_key=os.getenv("OPEN_AI"),base_url="https://openrouter.ai/api/v1")

def ask_chat_gpt(request:str) -> str:
    response = client.responses.create(
        model="gpt-5-nano",
        input=request
    )

    return response.output_text


#print(asyncio.run(ask_chat_gpt_async("привет")))

