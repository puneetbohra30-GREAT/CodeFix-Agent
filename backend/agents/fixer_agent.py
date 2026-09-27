class FixerAgent:
    def choose_fix(self, analysis):
        return analysis.get("fixed_code", "")
