"""Optional Gemini adapters. Any failure falls back to deterministic cached data."""
import json
import os
from .models import Bulletin
from .advisories import generate

MODEL = "gemini-3.7-flash"


def enabled():
    return bool(os.getenv("GEMINI_API_KEY")) and os.getenv("PRELANDFALL_DEMO") != "true"


def extract_bulletin(source: bytes, filename: str):
    if not enabled():
        return Bulletin(), "cached-demo"
    try:
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        prompt = "Extract cyclone bulletin facts. Return JSON matching: landfall_lat, landfall_lon, landfall_time (ISO), max_wind_kmph, pressure_hpa, track_points [[lat,lon]]. Do not infer missing facts."
        response = client.models.generate_content(model=MODEL, contents=[prompt, {"mime_type": "application/octet-stream", "data": source}], config={"response_mime_type": "application/json"})
        return Bulletin.model_validate_json(response.text), "gemini"
    except Exception:
        return Bulletin(), "cached-fallback"


def advisory_with_tools(level: str, audience: str, language: str, engine_metrics: dict):
    """Function-style data grounding: only engine_metrics are supplied to the model."""
    if not enabled():
        return generate(level, audience, language), "template"
    try:
        from google import genai
        client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
        prompt = ("Write a short early-warning advisory for the " + audience + " in " + language + ". "
                  "Use only these machine-calculated numbers and do not add any other number: " + json.dumps(engine_metrics) + ". "
                  "Mention this is a screening-level scenario.")
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text, "gemini-grounded"
    except Exception:
        return generate(level, audience, language), "template-fallback"
