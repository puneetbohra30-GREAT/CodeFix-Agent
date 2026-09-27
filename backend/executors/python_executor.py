import subprocess, sys, tempfile, time
from pathlib import Path
from .base_executor import BaseExecutor, ExecutionResult
from backend.config import EXECUTION_TIMEOUT

class PythonExecutor(BaseExecutor):
    def run(self, code):
        with tempfile.TemporaryDirectory(prefix="codefix_py_") as d:
            file = Path(d) / "main.py"
            file.write_text(code, encoding="utf-8")
            start = time.perf_counter()
            try:
                p = subprocess.run(
                    [sys.executable, str(file)],
                    capture_output=True, text=True,
                    timeout=EXECUTION_TIMEOUT,
                    cwd=d
                )
                ms = int((time.perf_counter()-start)*1000)
                return ExecutionResult(p.returncode == 0, p.stdout, p.stderr, ms)
            except subprocess.TimeoutExpired:
                return ExecutionResult(False, "", "Execution timed out.", EXECUTION_TIMEOUT*1000)
            except Exception as e:
                return ExecutionResult(False, "", str(e))
