from fastapi import APIRouter
import shutil

router = APIRouter(prefix="/api/health", tags=["Health"])

@router.get("")
def health():
    return {
        "status": "online",
        "app": "CodeFix Agent",
        "executors": {
            "python": "available",
            "cpp": shutil.which("g++") is not None,
            "java": shutil.which("java") is not None,
            "javac": shutil.which("javac") is not None
        }
    }
