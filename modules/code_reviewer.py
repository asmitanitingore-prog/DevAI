from utils.code_analysis import analyze_code


def review_code(code: str):
    """
    Run a complete code review and return the results.
    """

    if not code.strip():
        return {
            "error": "No code was provided."
        }

    analysis = analyze_code(code)

    return analysis