from abc import ABC, abstractmethod

class ExecutionResult:
    def __init__(self, success, output="", error="", duration_ms=0):
        self.success = success
        self.output = output
        self.error = error
        self.duration_ms = duration_ms

class BaseExecutor(ABC):
    @abstractmethod
    def run(self, code: str) -> ExecutionResult:
        pass
