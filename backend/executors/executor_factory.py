from .python_executor import PythonExecutor
from .cpp_executor import CppExecutor
from .java_executor import JavaExecutor

def get_executor(language):
    mapping = {
        "python": PythonExecutor,
        "cpp": CppExecutor,
        "java": JavaExecutor,
    }
    try:
        return mapping[language]()
    except KeyError:
        raise ValueError("Supported languages: Python, C++, Java.")
