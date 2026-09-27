import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "database" / "codefix.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS debug_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            language TEXT NOT NULL,
            error TEXT,
            original_code TEXT NOT NULL,
            fixed_code TEXT,
            root_cause TEXT,
            explanation TEXT,
            execution_output TEXT,
            status TEXT,
            attempts INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_session(data):
    conn = get_connection()
    cur = conn.execute("""
        INSERT INTO debug_sessions
        (language,error,original_code,fixed_code,root_cause,explanation,execution_output,status,attempts)
        VALUES (?,?,?,?,?,?,?,?,?)
    """, (
        data["language"], data.get("error",""), data["original_code"],
        data.get("fixed_code",""), data.get("root_cause",""),
        data.get("explanation",""), data.get("execution_output",""),
        data.get("status",""), data.get("attempts",0)
    ))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id

def list_sessions():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM debug_sessions ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_sessions():
    conn = get_connection()
    conn.execute("DELETE FROM debug_sessions")
    conn.commit()
    conn.close()
