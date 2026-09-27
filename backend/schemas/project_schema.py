from pydantic import BaseModel

class HealthResponse(BaseModel):
    language: str
    files_scanned: int
    lines_scanned: int
    errors_found: int
    errors_fixed: int
    remaining: int
    debug_cycles: int
    tests_passed: int
    tests_total: int
    overall_status: str
