from backend.services.scanner_service import ScannerService

class ScannerAgent:
    def __init__(self):
        self.service = ScannerService()

    def scan(self, zip_path, output_dir):
        files = self.service.scan_zip(zip_path, output_dir)
        return files, self.service.summarize(files)
