from fastapi import APIRouter
from backend.database import list_sessions, delete_sessions

router = APIRouter(prefix="/api/history", tags=["History"])

@router.get("")
def history():
    return list_sessions()

@router.delete("")
def clear_history():
    delete_sessions()
    return {"success": True}
