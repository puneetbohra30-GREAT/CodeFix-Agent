from backend.config import MAX_DEBUG_ATTEMPTS
from backend.executors.executor_factory import get_executor
from backend.agents.analyzer_agent import AnalyzerAgent
from backend.agents.fixer_agent import FixerAgent
from backend.agents.evaluator_agent import EvaluatorAgent

class DebugOrchestrator:
    def __init__(self):
        self.analyzer = AnalyzerAgent()
        self.fixer = FixerAgent()
        self.evaluator = EvaluatorAgent()

    def run(self, language, code, error):
        executor = get_executor(language)
        current_code = code
        feedback = error
        attempts = 0
        history = []
        final_analysis = {}

        while attempts < MAX_DEBUG_ATTEMPTS:
            attempts += 1
            analysis = self.analyzer.analyze(language, current_code, error, feedback)
            final_analysis = analysis
            fixed_code = self.fixer.choose_fix(analysis) or current_code
            result = executor.run(fixed_code)
            evaluation = self.evaluator.evaluate(result)
            history.append({
                "cycle": attempts,
                "root_cause": analysis.get("root_cause",""),
                "error_type": analysis.get("error_type",""),
                "execution_success": evaluation["passed"],
                "execution_error": evaluation["error"],
                "output": evaluation["output"],
                "duration_ms": evaluation["duration_ms"]
            })
            if evaluation["passed"]:
                return {
                    "success": True,
                    "language": language,
                    "root_cause": analysis.get("root_cause",""),
                    "fixed_code": fixed_code,
                    "explanation": analysis.get("explanation",""),
                    "execution_output": evaluation["output"],
                    "attempts": attempts,
                    "status": "fixed",
                    "error_type": analysis.get("error_type",""),
                    "line": analysis.get("line"),
                    "history": history
                }
            current_code = fixed_code
            feedback = evaluation["error"] or "Execution failed. Re-check the corrected code."

        return {
            "success": False,
            "language": language,
            "root_cause": final_analysis.get("root_cause","Unable to fully resolve the issue."),
            "fixed_code": current_code,
            "explanation": final_analysis.get("explanation","The maximum debugging cycles were reached."),
            "execution_output": history[-1]["execution_error"] if history else "",
            "attempts": attempts,
            "status": "needs_attention",
            "error_type": final_analysis.get("error_type",""),
            "line": final_analysis.get("line"),
            "history": history
        }
