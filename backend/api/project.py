from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil, uuid
from backend.agents.scanner_agent import ScannerAgent
from backend.services.health_service import build_health

router = APIRouter(prefix="/api/project", tags=["Project"])
UPLOAD_ROOT = Path("uploads")
UPLOAD_ROOT.mkdir(exist_ok=True)
scanner = ScannerAgent()

@router.post("/scan")
async def scan_project(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Upload a ZIP project.")
    job = UPLOAD_ROOT / uuid.uuid4().hex
    job.mkdir(parents=True, exist_ok=True)
    zip_path = job / "project.zip"
    with zip_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)
    try:
        files, summary = scanner.scan(zip_path, job / "source")
        health = build_health(files)
        return {
            "success": True,
            "summary": summary,
            "files": [{"file": f["file"], "language": f["language"], "lines": f["lines"]} for f in files],
            "health": health
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
