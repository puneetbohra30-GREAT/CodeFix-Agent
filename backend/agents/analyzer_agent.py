from backend.services.gemini_service import GeminiService

class AnalyzerAgent:
    def __init__(self):
        self.ai = GeminiService()

    def analyze(self, language, code, error, feedback=""):
        return self.ai.analyze_and_fix(language, code, error, feedback)
