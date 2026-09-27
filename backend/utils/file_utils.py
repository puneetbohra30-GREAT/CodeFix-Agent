from pathlib import Path
import zipfile
import shutil

ALLOWED = {".py", ".cpp", ".cc", ".cxx", ".java"}

def safe_extract_zip(zip_path: Path, destination: Path):
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as z:
        for member in z.infolist():
            target = (destination / member.filename).resolve()
            if not str(target).startswith(str(destination.resolve())):
                raise ValueError("Unsafe ZIP path detected.")
        z.extractall(destination)

def scan_source_tree(root: Path):
    result = []
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in ALLOWED:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
                result.append({
                    "file": str(path.relative_to(root)),
                    "language": {".py":"python",".cpp":"cpp",".cc":"cpp",".cxx":"cpp",".java":"java"}[path.suffix.lower()],
                    "lines": len(text.splitlines()),
                    "code": text[:12000]
                })
            except OSError:
                pass
    return result
