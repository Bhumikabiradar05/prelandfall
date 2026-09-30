import os
from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from .models import Bulletin
from .engine import scenario, metrics
from .advisories import validate
from .gemini import extract_bulletin, advisory_with_tools

router = APIRouter()


class AdvisoryRequest(BaseModel):
    level: str = "mid"
    audience: str = "commissioner"
    language: str = "English"


class DispatchRequest(AdvisoryRequest):
    text: str


@router.get("/scenario/{level}")
def get_scenario(level: str):
    return scenario(level)


@router.post("/bulletin/manual")
def manual_bulletin(bulletin: Bulletin):
    return {"source": "manual", "bulletin": bulletin, "scenario": scenario("mid")}


@router.post("/bulletin/upload")
async def upload_bulletin(file: UploadFile):
    if not file.filename:
        raise HTTPException(400, "Choose an IMD bulletin first")
    bulletin, source = extract_bulletin(await file.read(), file.filename)
    return {"source": source, "filename": file.filename, "bulletin": bulletin}


@router.post("/advisories")
def advisory(request: AdvisoryRequest):
    engine_metrics = metrics(request.level)
    text, source = advisory_with_tools(request.level, request.audience, request.language, engine_metrics)
    return {"text": text, "source": source, "validation": validate(text, request.level), "metrics": engine_metrics}


@router.post("/dispatch")
def dispatch(request: DispatchRequest):
    check = validate(request.text, request.level)
    if not check["valid"]:
        raise HTTPException(422, detail={"message": "Advisory contains numbers not produced by the risk engine", **check})
    if os.getenv("PRELANDFALL_DEMO", "false") == "true":
        return {"sent": True, "mode": "mock", "message": "Demo dispatch recorded; no external message was sent."}
    return {"sent": False, "mode": "safe", "message": "Configure Telegram/email dispatch before enabling production sends."}
