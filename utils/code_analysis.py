import ast
from radon.complexity import cc_visit
from radon.metrics import mi_visit


def analyze_code(code: str):
    """Analyze Python source code and return structured results."""

    result = {
        "syntax_valid": True,
        "syntax_error": None,
        "lines": len(code.splitlines()),
        "functions": 0,
        "classes": 0,
        "complexity": 0,
        "maintainability": 0,
        "issues": [],
        "score": 100,
    }

    # -------------------------
    # Syntax analysis
    # -------------------------
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        result["syntax_valid"] = False
        result["syntax_error"] = f"Line {e.lineno}: {e.msg}"
        result["score"] = 0
        return result

    # -------------------------
    # AST analysis
    # -------------------------
    functions = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]

    classes = [
        node for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]

    result["functions"] = len(functions)
    result["classes"] = len(classes)

    # -------------------------
    # Cyclomatic complexity
    # -------------------------
    try:
        complexity_data = cc_visit(code)

        if complexity_data:
            result["complexity"] = round(
                sum(item.complexity for item in complexity_data)
                / len(complexity_data),
                2
            )
    except Exception:
        result["complexity"] = 0

    # -------------------------
    # Maintainability index
    # -------------------------
    try:
        result["maintainability"] = round(
            mi_visit(code, multi=True),
            2
        )
    except Exception:
        result["maintainability"] = 0

    # -------------------------
    # Code quality checks
    # -------------------------

    for node in ast.walk(tree):

        # eval()
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):

                if node.func.id == "eval":
                    result["issues"].append({
                        "type": "Security",
                        "message": "Avoid eval(). It can execute arbitrary code.",
                        "line": node.lineno
                    })

                # exec()
                elif node.func.id == "exec":
                    result["issues"].append({
                        "type": "Security",
                        "message": "Avoid exec(). It can execute arbitrary code.",
                        "line": node.lineno
                    })

                # print()
                elif node.func.id == "print":
                    result["issues"].append({
                        "type": "Quality",
                        "message": "Consider using logging instead of print() in production code.",
                        "line": node.lineno
                    })

        # Bare except
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                result["issues"].append({
                    "type": "Quality",
                    "message": "Avoid bare 'except'. Catch specific exceptions.",
                    "line": node.lineno
                })

    # -------------------------
    # Long functions
    # -------------------------

    for function in functions:

        if hasattr(function, "end_lineno") and function.end_lineno:
            length = function.end_lineno - function.lineno + 1

            if length > 40:
                result["issues"].append({
                    "type": "Maintainability",
                    "message": (
                        f"Function '{function.name}' is {length} lines long. "
                        "Consider splitting it into smaller functions."
                    ),
                    "line": function.lineno
                })

    # -------------------------
    # Calculate score
    # -------------------------

    score = 100

    for issue in result["issues"]:

        if issue["type"] == "Security":
            score -= 20

        elif issue["type"] == "Maintainability":
            score -= 10

        else:
            score -= 5

    # Complexity penalty
    if result["complexity"] > 10:
        score -= 15
    elif result["complexity"] > 5:
        score -= 5

    result["score"] = max(0, min(100, score))

    return result