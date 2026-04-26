from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import json
import math
import os

from main import run_hey_agent

app = FastAPI(title="Hey Banco Proactive API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir API y estáticos
@app.get("/")
def read_root():
    return FileResponse("frontend/index.html")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

def safe_isnan(val):
    if isinstance(val, float) and math.isnan(val):
        return True
    return False

@app.get("/api/users")
def get_users():
    try:
        df = pd.read_csv('data/df_profiles.csv')
        users = df[['user_id']].drop_duplicates().head(50).to_dict(orient='records')
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/{user_id}")
def get_dashboard_data(user_id: str):
    try:
        df_profile = pd.read_csv('data/multi_mapper_profile_final.csv')
        profile_data = df_profile[df_profile['user_id'] == user_id]
        
        if profile_data.empty:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en perfiles")
            
        profile = profile_data.iloc[0].to_dict()
        for k, v in profile.items():
            if safe_isnan(v):
                profile[k] = None
        
        df_tx = pd.read_csv('data/hey_transacciones.csv')
        tx_data = df_tx[df_tx['user_id'] == user_id]
        
        tx_list = tx_data.tail(10).to_dict(orient='records')
        for tx in tx_list:
            for k, v in tx.items():
                if safe_isnan(v):
                    tx[k] = None

        return {
            "profile": profile,
            "transactions": tx_list
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze/{user_id}")
def analyze_user(user_id: str):
    try:
        result = run_hey_agent(user_id)
        return {"user_id": user_id, "analysis": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from pydantic import BaseModel
from typing import List

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage]

@app.post("/api/chat/{user_id}")
def chat_endpoint(user_id: str, req: ChatRequest):
    try:
        from main import chat_with_agent
        reply = chat_with_agent(user_id, req.message, [h.model_dump() for h in req.history])
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

