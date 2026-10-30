import re
import ast


def analyze_bug(code: str, error_message: str):
    """Analyze Python code and an error message."""

    result = {
        "error_type": "Unknown",
        "error_message": error_message.strip(),
        "cause": "Unable to determine the exact cause.",
        "suggestion": "Review the traceback and check the relevant line.",
    }

    # Detect error type
    match = re.search(
        r"([A-Za-z]+Error|[A-Za-z]+Exception)",
        error_message
    )

    if match:
        error_type = match.group(1)
        result["error_type"] = error_type

    # Common Python errors
    if "NameError" in error_message:
        result["cause"] = (
            "A variable or function was used before it was defined."
        )
        result["suggestion"] = (
            "Check the variable name, spelling, and whether it was "
            "defined before use."
        )

    elif "TypeError" in error_message:
        result["cause"] = (
            "An operation or function received a value of an "
            "incompatible type."
        )
        result["suggestion"] = (
            "Check the data types of the values being passed to "
            "the operation or function."
        )

    elif "IndexError" in error_message:
        result["cause"] = (
            "The code tried to access a list or sequence index "
            "that does not exist."
        )
        result["suggestion"] = (
            "Check the list length and make sure the index is "
            "within the valid range."
        )

    elif "KeyError" in error_message:
        result["cause"] = (
            "A dictionary key that does not exist was accessed."
        )
        result["suggestion"] = (
            "Check whether the key exists before accessing it, "
            "or use dict.get()."
        )

    elif "ZeroDivisionError" in error_message:
        result["cause"] = (
            "The program attempted to divide a number by zero."
        )
        result["suggestion"] = (
            "Validate the denominator before performing division."
        )

    elif "SyntaxError" in error_message:
        result["cause"] = (
            "Python could not understand the structure of the code."
        )
        result["suggestion"] = (
            "Check brackets, indentation, colons, quotes, and "
            "Python syntax near the reported line."
        )

    # Validate source code
    if code.strip():

        try:
            ast.parse(code)

        except SyntaxError as e:

            result["suggestion"] += (
                f" The source code itself has a syntax problem "
                f"near line {e.lineno}."
            )

    return result