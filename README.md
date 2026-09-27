# ⚡ CodeFix Agent

Autonomous AI Coding Debugger for **Python, C++ and Java**.

## Hackathon problem

CodeFix Agent addresses PS-06: accept source code plus an error/problem, analyze likely issues, suggest a correction with an explanation, use execution/testing feedback, and perform multiple debugging cycles.

## Agent loop

`Input → Analyze → Fix → Execute → Evaluate → Retry/Verify`

The application uses Gemini when `GEMINI_API_KEY` is configured. Without an API key, it still has deterministic demo fallbacks for the included examples.

## Features

- Python, C++, Java
- Execution feedback from real local interpreters/compilers
- Up to 3 repair cycles
- Root-cause and explanation output
- ZIP codebase scanner
- Codebase Health dashboard
- SQLite debug history
- Colorful browser UI
- FastAPI Swagger API

## Setup — Windows

### 1. Create Python environment

```powershell
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

### 2. Configure Gemini

Copy `.env.example` to `.env` and add your Gemini API key if available.

### 3. Verify tools

```powershell
python --version
g++ --version
java -version
javac -version
```

### 4. Start backend

```powershell
uvicorn backend.main:app --reload
```

Open Swagger: http://127.0.0.1:8000/docs

### 5. Start frontend

Open `frontend/index.html` with VS Code Live Server.

Do not type `Live Server` as a PowerShell command.

## Safety note

The executor uses temporary directories, subprocesses and timeouts. This is suitable for a controlled local hackathon demo. A public deployment that accepts arbitrary untrusted code should use a hardened sandbox/container isolation layer.

## Submission

Include the GitHub repository, working prototype/deployed application where applicable, and this README. The hackathon guidance asks teams to explain the problem, solution, setup and major components.
