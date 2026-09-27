EXTENSIONS = {
    ".py": "python",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".java": "java",
}

def language_from_filename(name: str):
    import os
    return EXTENSIONS.get(os.path.splitext(name)[1].lower())

def normalize_language(language: str) -> str:
    value = language.strip().lower()
    aliases = {"c++": "cpp", "cplusplus": "cpp", "py": "python", "java": "java"}
    value = aliases.get(value, value)
    if value not in {"python", "cpp", "java"}:
        raise ValueError("Only Python, C++, and Java are supported.")
    return value
