import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()
_API_KEY = os.getenv("TOGETHER_API_KEY")  # Make sure .env has this
_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
_BASE_URL = "https://api.together.xyz/v1/chat/completions"

print("✅ TOGETHER_API_KEY:", _API_KEY[:6] + "..." if _API_KEY else "❌ Not Loaded")

def _chat(messages, **params):
    headers = {
        "Authorization": f"Bearer {_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": _MODEL,
        "messages": messages,
        **params
    }

    r = requests.post(_BASE_URL, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def parse_user_query(query: str) -> dict:
    system = {
        "role": "system",
        "content": (
            "Convert user queries into strict valid JSON. "
            "Do not include markdown, explanations, or extra text. "
            "Return only raw JSON like:\n"
            '{ "type": "product", "keywords": "iPhone", "currency": "INR", "max_price": 60000, "sites": ["amazon"] }\n'
            '{ "type": "flight", "origin": "Delhi", "destination": "Mumbai", "date": "2025-08-05" }'
        )
    }

    user = {
        "role": "user",
        "content": query
    }

    raw = _chat([system, user], temperature=0)
    print("🔍 LLM Raw Output:\n", raw)

    # Extract the first JSON-like block
    match = re.search(r"\{.*?\}", raw, re.DOTALL)
    if not match:
        raise ValueError("❌ Could not find JSON in LLM output")

    json_str = match.group(0)

    try:
        parsed = json.loads(json_str)
        return parsed
    except json.JSONDecodeError as e:
        print("❌ JSON parsing failed:", e)
        print("⚠️ Extracted JSON:", json_str)
        raise e
