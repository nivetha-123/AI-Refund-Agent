#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 14:24:09 2026

@author: nivetha
"""
import os
import json
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from models.database import init_db, get_conn
from agent import run_agent_stream

app = FastAPI(title="Worknoon Refund Agent API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()
    print("🚀 API started")


# ── Models ───────────────────────────────────────────────────
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    session_id: Optional[str] = None


# ── Endpoints ────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(req: ChatRequest):

    messages = [
        {
            "role": m.role,
            "content": m.content
        }
        for m in req.messages
    ]

    logs = []
    final_response = None

    for event in run_agent_stream(messages):

        print(event)

        logs.append(event)

        if event["type"] == "final":
            final_response = event

    return {
        "decision": final_response["decision"],
        "response": final_response["response"],
        "logs": logs
    }
@app.get("/admin/customers")
def list_customers():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()
    conn.close()
    return {"customers": [dict(r) for r in rows]}


@app.get("/admin/orders")
def list_orders():
    conn = get_conn()
    rows = conn.execute(
        """SELECT o.*, c.name as customer_name, c.account_tier
           FROM orders o JOIN customers c ON o.customer_email = c.email
           ORDER BY o.id"""
    ).fetchall()
    conn.close()
    return {"orders": [dict(r) for r in rows]}


@app.get("/customer/{email}")
def get_customer(email: str):
    from tools.refund_tools import lookup_customer
    return lookup_customer(email)


@app.get("/order/{order_id}")
def get_order(order_id: str):
    from tools.refund_tools import lookup_order
    return lookup_order(order_id)
