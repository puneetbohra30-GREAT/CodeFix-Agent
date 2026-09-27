import subprocess, tempfile, time
from pathlib import Path
from .base_executor import BaseExecutor, ExecutionResult
from backend.config import EXECUTION_TIMEOUT

class JavaExecutor(BaseExecutor):
    def run(self, code):
        with tempfile.TemporaryDirectory(prefix="codefix_java_") as d:
            src = Path(d) / "Main.java"
            src.write_text(code, encoding="utf-8")
            start = time.perf_counter()
            try:
                compile_p = subprocess.run(
                    ["javac", str(src)],
                    capture_output=True, text=True, timeout=EXECUTION_TIMEOUT, cwd=d
                )
                if compile_p.returncode != 0:
                    return ExecutionResult(False, "", compile_p.stderr, int((time.perf_counter()-start)*1000))
                run_p = subprocess.run(
                    ["java", "-cp", d, "Main"],
                    capture_output=True, text=True,
                    timeout=EXECUTION_TIMEOUT, cwd=d
                )
                return ExecutionResult(
                    run_p.returncode == 0, run_p.stdout, run_p.stderr,
                    int((time.perf_counter()-start)*1000)
                )
            except FileNotFoundError:
                return ExecutionResult(False, "", "Java/Javac was not found in PATH.")
            except subprocess.TimeoutExpired:
                return ExecutionResult(False, "", "Execution timed out.", EXECUTION_TIMEOUT*1000)
            except Exception as e:
                return ExecutionResult(False, "", str(e))
