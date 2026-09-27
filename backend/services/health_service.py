def build_health(files, errors_found=0, errors_fixed=0, debug_cycles=0, tests_passed=0, tests_total=0):
    remaining = max(errors_found - errors_fixed, 0)
    return {
        "language": ", ".join(files and sorted(set(f["language"] for f in files)) or ["Unknown"]),
        "files_scanned": len(files),
        "lines_scanned": sum(f["lines"] for f in files),
        "errors_found": errors_found,
        "errors_fixed": errors_fixed,
        "remaining": remaining,
        "debug_cycles": debug_cycles,
        "tests_passed": tests_passed,
        "tests_total": tests_total,
        "overall_status": "HEALTHY" if remaining == 0 else "NEEDS ATTENTION"
    }
