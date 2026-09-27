from pathlib import Path
import tempfile
import shutil

def temporary_directory():
    return tempfile.TemporaryDirectory(prefix="codefix_")

def cleanup_path(path: Path):
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
