"""
ClauseGuard AI — FastAPI Server
Serves the frontend and provides API endpoints for contract analysis.
"""

import os
import uuid
import json
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from agents import ContractAgentPipeline

load_dotenv(Path(__file__).parent.parent / ".env")

app = FastAPI(title="ClauseGuard AI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
UPLOAD_DIR = Path(__file__).parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

contracts: dict = {}

ALLOWED_TYPES = {
    "application/pdf",
    "image/png",
    "image/jpeg",
    "image/webp",
    "image/jpg",
}

FRONTEND = Path(__file__).parent.parent / "frontend"


@app.get("/api/health")
async def health():
    return {"status": "ok", "gemini_configured": bool(GEMINI_API_KEY)}


@app.post("/api/upload")
async def upload_contract(file: UploadFile = File(...)):
    if not GEMINI_API_KEY:
        raise HTTPException(500, "GEMINI_API_KEY is not set. Add it to your .env file.")

    ct = file.content_type or ""
    if ct not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {ct}. Use PDF, PNG, JPG, or WebP.")

    contract_id = uuid.uuid4().hex[:12]
    ext = (file.filename or "file").rsplit(".", 1)[-1]
    dest = UPLOAD_DIR / f"{contract_id}.{ext}"
    content = await file.read()
    dest.write_bytes(content)

    contracts[contract_id] = {
        "id": contract_id,
        "filename": file.filename,
        "file_path": str(dest),
        "content_type": ct,
        "status": "uploaded",
        "results": None,
    }
    return {"contract_id": contract_id, "filename": file.filename}


@app.get("/api/analyze/{contract_id}")
async def analyze(contract_id: str):
    if contract_id not in contracts:
        raise HTTPException(404, "Contract not found")

    c = contracts[contract_id]

    async def stream():
        pipeline = ContractAgentPipeline(GEMINI_API_KEY)
        try:
            async for event in pipeline.run(c["file_path"], c["content_type"]):
                yield f"data: {json.dumps(event)}\n\n"
                if event.get("type") == "pipeline_complete":
                    contracts[contract_id]["results"] = event["data"]
                    contracts[contract_id]["status"] = "complete"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
        yield f"data: {json.dumps({'type': 'stream_end'})}\n\n"

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )


@app.get("/api/results/{contract_id}")
async def results(contract_id: str):
    if contract_id not in contracts:
        raise HTTPException(404, "Contract not found")
    return contracts[contract_id]


# ── Static files BEFORE the catch-all ───────────────────────
app.mount("/css", StaticFiles(directory=str(FRONTEND / "css")), name="css")
app.mount("/js", StaticFiles(directory=str(FRONTEND / "js")), name="js")


@app.get("/")
async def index():
    html = (FRONTEND / "index.html").read_text(encoding="utf-8")
    return HTMLResponse(html)
