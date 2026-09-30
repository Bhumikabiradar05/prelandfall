import argparse
import os
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.api import router

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")
app = FastAPI(title="PreLandfall", version="0.1.0")
app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory=ROOT / "frontend"), name="static")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(ROOT / "frontend" / "index.html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PreLandfall local prototype")
    parser.add_argument("--demo", action="store_true", help="Use only cached fixtures and mock dispatch")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    os.environ["PRELANDFALL_DEMO"] = str(args.demo).lower()
    uvicorn.run(app, host="127.0.0.1", port=args.port)
