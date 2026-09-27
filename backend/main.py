from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import init_db
from backend.api import health, debug, project, history

app = FastAPI(title="CodeFix Agent", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(health.router)
app.include_router(debug.router)
app.include_router(project.router)
app.include_router(history.router)

@app.get("/")
def root():
    return {
        "name": "CodeFix Agent",
        "message": "Autonomous AI Coding Debugger",
        "supported_languages": ["Python", "C++", "Java"]
    }
