from pydantic import BaseModel, Field

class DebugRequest(BaseModel):
    language: str
    code: str = Field(min_length=1)
    error: str = ""

class DebugResponse(BaseModel):
    success: bool
    language: str
    root_cause: str
    fixed_code: str
    explanation: str
    execution_output: str
    attempts: int
    status: str
    error_type: str = ""
    line: int | None = None
