import subprocess, tempfile, time
from pathlib import Path
from .base_executor import BaseExecutor, ExecutionResult
from backend.config import EXECUTION_TIMEOUT

class CppExecutor(BaseExecutor):
    def run(self, code):
        with tempfile.TemporaryDirectory(prefix="codefix_cpp_") as d:
            src = Path(d) / "main.cpp"
            exe = Path(d) / "main.exe"
            src.write_text(code, encoding="utf-8")
            start = time.perf_counter()
            try:
                compile_p = subprocess.run(
                    ["g++", "-std=c++17", str(src), "-o", str(exe)],
                    capture_output=True, text=True, timeout=EXECUTION_TIMEOUT
                )
                if compile_p.returncode != 0:
                    return ExecutionResult(False, "", compile_p.stderr, int((time.perf_counter()-start)*1000))
                run_p = subprocess.run(
                    [str(exe)], capture_output=True, text=True,
                    timeout=EXECUTION_TIMEOUT, cwd=d
                )
                return ExecutionResult(
                    run_p.returncode == 0, run_p.stdout, run_p.stderr,
                    int((time.perf_counter()-start)*1000)
                )
            except FileNotFoundError:
                return ExecutionResult(False, "", "g++ was not found in PATH.")
            except subprocess.TimeoutExpired:
                return ExecutionResult(False, "", "Execution timed out.", EXECUTION_TIMEOUT*1000)
            except Exception as e:
                return ExecutionResult(False, "", str(e))
