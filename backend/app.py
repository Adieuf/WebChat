import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from dotenv import load_dotenv

load_dotenv()

DIRECT_LINE_SECRET = os.getenv('DIRECT_LINE_SECRET')
DIRECT_LINE_URL = "https://directline.botframework.com/v3/directline/tokens/generate"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

class TokenResponse(BaseModel):
    token: str

@app.get('/api/token', response_model=TokenResponse)
def generate_token():
    if not DIRECT_LINE_SECRET:
        raise HTTPException(status_code=500, detail='DIRECT_LINE_SECRET not configured')
    headers = {
        'Authorization': f'Bearer {DIRECT_LINE_SECRET}'
    }
    resp = requests.post(DIRECT_LINE_URL, headers=headers)
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    data = resp.json()
    return TokenResponse(token=data['token'])
