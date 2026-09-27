from pathlib import Path
from backend.utils.file_utils import safe_extract_zip, scan_source_tree

class ScannerService:
    def scan_zip(self, zip_path, output_dir):
        safe_extract_zip(Path(zip_path), Path(output_dir))
        files = scan_source_tree(Path(output_dir))
        return files

    def summarize(self, files):
        return {
            "files_scanned": len(files),
            "lines_scanned": sum(x["lines"] for x in files),
            "languages": sorted(set(x["language"] for x in files))
        }
