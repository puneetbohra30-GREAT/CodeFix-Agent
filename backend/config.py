import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "CodeFix Agent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_DEBUG_ATTEMPTS = int(os.getenv("MAX_DEBUG_ATTEMPTS", "3"))
EXECUTION_TIMEOUT = int(os.getenv("EXECUTION_TIMEOUT", "5"))
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "2"))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
