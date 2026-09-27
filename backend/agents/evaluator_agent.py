class EvaluatorAgent:
    def evaluate(self, result):
        return {
            "passed": result.success,
            "output": result.output,
            "error": result.error,
            "duration_ms": result.duration_ms
        }
