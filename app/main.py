from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Literal
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

app = FastAPI(title="TouchGrass AI", description="A local-first outdoor mission generator powered by an open-weight model.", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

class MissionRequest(BaseModel):
    activity: Literal["any", "walking", "gardening", "birdwatching", "photography", "running", "mindfulness", "exploring"] = "any"
    duration: int = Field(default=20, ge=5, le=180)
    energy: Literal["low", "medium", "high"] = "medium"
    setting: Literal["backyard", "park", "neighborhood", "trail", "balcony", "anywhere"] = "anywhere"
    accessibility: str = Field(default="", max_length=240)
    avoid: str = Field(default="", max_length=240)

class Mission(BaseModel):
    title: str
    why: str
    checklist: list[str]
    mindful_prompt: str
    safety_note: str
    estimated_minutes: int

SYSTEM_PROMPT = """You are TouchGrass, a thoughtful outdoor activity designer. Create small, practical missions that get a person away from their screen and into the physical world. The user may be in a city, at home, or have limited mobility. Never assume access to a car, expensive equipment, private land, or wilderness. Respect accessibility needs and avoid the user's listed exclusions. Do not recommend trespassing, touching wildlife, eating unknown plants/mushrooms, approaching dangerous animals, or entering unsafe areas. Keep the activity low-risk and suitable for the stated duration and energy. Avoid medical claims. Return ONLY valid JSON with exactly these keys: title (short string), why (one sentence), checklist (array of 3 to 5 short actionable strings), mindful_prompt (one sentence to notice the real world), safety_note (short practical safety reminder), estimated_minutes (integer). No markdown fences."""

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/api/health")
def health():
    return {"status": "ok", "model": OLLAMA_MODEL, "provider": "local Ollama / open-weight model", "local_first": True}

@app.post("/api/mission", response_model=Mission)
def create_mission(data: MissionRequest):
    user_details = {
        "activity_preference": data.activity,
        "available_minutes": data.duration,
        "energy_level": data.energy,
        "setting": data.setting,
        "accessibility_needs": data.accessibility.strip() or "None specified",
        "things_to_avoid": data.avoid.strip() or "None specified",
    }
    prompt = "Create one outdoor mission for these preferences. Make it possible to begin within five minutes and keep the phone use to a minimum. Preferences: " + json.dumps(user_details, ensure_ascii=False)
    payload = json.dumps({"model": OLLAMA_MODEL, "system": SYSTEM_PROMPT, "prompt": prompt, "stream": False, "format": "json", "options": {"temperature": 0.75}}).encode()
    req = Request(OLLAMA_URL.rstrip("/") + "/api/generate", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=90) as response:
            result = json.loads(response.read().decode("utf-8"))
        raw = result.get("response", "")
        # Defensive extraction in case a model includes surrounding text.
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if not match:
            raise ValueError("Model did not return JSON")
        parsed = json.loads(match.group(0))
        mission = Mission(**parsed)
        mission.estimated_minutes = max(5, min(data.duration, mission.estimated_minutes))
        mission.checklist = mission.checklist[:5]
        if len(mission.checklist) < 3:
            raise ValueError("Model returned too few steps")
        return mission
    except (URLError, HTTPError, TimeoutError) as exc:
        raise HTTPException(status_code=503, detail=f"Local model unavailable. Start Ollama and download '{OLLAMA_MODEL}'. Details: {exc}") from exc
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=502, detail="The local model returned an unexpected response. Try generating another mission.") from exc
