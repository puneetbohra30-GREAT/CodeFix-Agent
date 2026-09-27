from fastapi import APIRouter, HTTPException
from backend.schemas.debug_schema import DebugRequest
from backend.agents.orchestrator import DebugOrchestrator
from backend.database import save_session

router = APIRouter(prefix="/api/debug", tags=["Debug"])
orchestrator = DebugOrchestrator()

@router.post("")
def debug_code(request: DebugRequest):
    try:
        language = request.language.strip().lower()
        if language == "c++":
            language = "cpp"
        result = orchestrator.run(language, request.code, request.error)
        save_session({
            "language": language,
            "error": request.error,
            "original_code": request.code,
            "fixed_code": result["fixed_code"],
            "root_cause": result["root_cause"],
            "explanation": result["explanation"],
            "execution_output": result["execution_output"],
            "status": result["status"],
            "attempts": result["attempts"]
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
