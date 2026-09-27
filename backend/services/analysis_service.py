def merge_feedback(error, execution_result):
    parts = []
    if error:
        parts.append("Reported problem:\n" + error)
    if execution_result:
        parts.append("Latest execution feedback:\n" + execution_result)
    return "\n\n".join(parts)
