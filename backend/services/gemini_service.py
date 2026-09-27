import json

from backend.config import GEMINI_API_KEY, GEMINI_MODEL


class GeminiService:

    def __init__(self):
        self.enabled = bool(GEMINI_API_KEY)
        self.client = None

        if self.enabled:
            try:
                from google import genai

                self.client = genai.Client(
                    api_key=GEMINI_API_KEY
                )

            except Exception as e:
                print("Gemini initialization error:", e)
                self.enabled = False

    def analyze_and_fix(
        self,
        language,
        code,
        error,
        execution_feedback=""
    ):

        # Gemini available
        if self.enabled and self.client:

            prompt = f"""
You are an expert debugging assistant.

Language: {language}

Source code:
{code}

Reported error:
{error}

Previous execution feedback:
{execution_feedback}

Analyze the actual error.

Return ONLY valid JSON:

{{
    "root_cause": "actual root cause",
    "error_type": "actual error type",
    "line": null,
    "fixed_code": "complete corrected code",
    "explanation": "clear explanation"
}}
"""

            try:
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt
                )

                text = response.text.strip()

                # Remove markdown fences if Gemini adds them
                if text.startswith("```json"):
                    text = text[7:]

                if text.startswith("```"):
                    text = text[3:]

                if text.endswith("```"):
                    text = text[:-3]

                text = text.strip()

                data = json.loads(text)

                return {
                    "root_cause": data.get(
                        "root_cause",
                        "Unknown error"
                    ),
                    "error_type": data.get(
                        "error_type",
                        "Unknown"
                    ),
                    "line": data.get(
                        "line",
                        None
                    ),
                    "fixed_code": data.get(
                        "fixed_code",
                        code
                    ),
                    "explanation": data.get(
                        "explanation",
                        "Code analyzed."
                    )
                }

            except Exception as e:

                print("Gemini API error:", e)

        # Fallback when Gemini is unavailable
        return self.local_fallback(
            language,
            code,
            error,
            execution_feedback
        )

    def local_fallback(
        self,
        language,
        code,
        error,
        feedback=""
    ):

        error_text = (
            str(error) + "\n" + str(feedback)
        ).lower()

        error_type = "Unknown Error"

        if "syntaxerror" in error_text:
            error_type = "SyntaxError"

        elif "nameerror" in error_text:
            error_type = "NameError"

        elif "typeerror" in error_text:
            error_type = "TypeError"

        elif "indexerror" in error_text:
            error_type = "IndexError"

        elif "zerodivisionerror" in error_text:
            error_type = "ZeroDivisionError"

        elif "timeout" in error_text:
            error_type = "Timeout"

        elif "arrayindexoutofboundsexception" in error_text:
            error_type = "ArrayIndexOutOfBoundsException"

        elif "nullpointerexception" in error_text:
            error_type = "NullPointerException"

        elif "compilation" in error_text:
            error_type = "Compilation Error"

        return {
            "root_cause": (
                "The submitted program contains an error "
                "reported by the execution system."
            ),
            "error_type": error_type,
            "line": None,
            "fixed_code": code,
            "explanation": (
                "The actual execution error was identified "
                "from the available execution feedback."
            )
        }