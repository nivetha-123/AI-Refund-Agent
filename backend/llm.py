#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 27 15:22:10 2026

@author: nivetha
"""

import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def generate_response(prompt):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": "You are a refund support AI."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0
    )

    return completion.choices[0].message.content
