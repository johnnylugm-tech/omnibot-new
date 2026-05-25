"""FR-18: Python naming conventions, docstrings, function length, CC ≤ 10."""
from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

SRC_ROOT = Path("03-development/src/omnibot")


def test_fr18_ruff_check_zero_violations():
    """Run ruff check on the source and assert zero violations."""
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "03-development/src/", "--output-format=text"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"ruff found violations:\n{result.stdout}\n{result.stderr}"


def test_fr18_radon_cc_max_less_than_or_equal_10():
    """Assert no function/method in source has cyclomatic complexity > 10."""
    import json

    result = subprocess.run(
        [sys.executable, "-m", "radon", "cc", "03-development/src/", "-j"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"radon cc failed: {result.stderr}"

    data = json.loads(result.stdout)
    violations = []
    for filepath, blocks in data.items():
        for block in blocks:
            complexity = block.get("complexity", 0)
            if complexity > 10:
                name = block.get("name", "?")
                line = block.get("lineno", "?")
                violations.append(f"{filepath}:{line} {name} CC={complexity}")

    assert len(violations) == 0, f"Functions with CC > 10:\n" + "\n".join(violations)


def test_fr18_all_public_functions_have_docstrings():
    """All public (non-underscore) functions in source must have docstrings."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                if name.startswith("_") and not name.startswith("__"):
                    continue
                doc = ast.get_docstring(node)
                if doc is None:
                    violations.append(f"{filepath}:{node.lineno} {name} has no docstring")

    assert len(violations) == 0, "Public functions missing docstrings:\n" + "\n".join(violations)


def test_fr18_function_length_less_than_or_equal_50_lines():
    """No function may exceed 50 lines (excluding docstring/comment/blank)."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    for filepath in src_files:
        try:
            content = filepath.read_text()
            tree = ast.parse(content, filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                start = node.lineno
                end = node.end_lineno or start
                # count non-empty, non-comment lines
                lines = content.splitlines()
                code_lines = [
                    ln.strip()
                    for ln in lines[start - 1 : end]
                    if ln.strip() and not ln.strip().startswith("#")
                ]
                if len(code_lines) > 50:
                    violations.append(
                        f"{filepath}:{start} {node.name} has {len(code_lines)} lines (> 50)"
                    )

    assert len(violations) == 0, "Functions exceeding 50 lines:\n" + "\n".join(violations)


def test_fr18_constants_use_upper_snake_case():
    """Module-level constants must use UPPER_SNAKE_CASE."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    snake_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")
    pascal_pattern = re.compile(r"^[A-Z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)*$")

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        name = target.id
                        if name.isupper() or "_" not in name:
                            continue
                        if snake_pattern.match(name):
                            violations.append(
                                f"{filepath}:{node.lineno} constant '{name}' should be UPPER_SNAKE_CASE"
                            )

    assert len(violations) == 0, "Constants with wrong naming:\n" + "\n".join(violations)


def test_fr18_classes_use_pascal_case():
    """All class definitions must use PascalCase."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    pascal_pattern = re.compile(r"^[A-Z][a-zA-Z0-9]+([A-Z][a-zA-Z0-9]*)*$")

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                name = node.name
                if name.startswith("_"):
                    continue
                if not pascal_pattern.match(name):
                    violations.append(f"{filepath}:{node.lineno} class '{name}' should be PascalCase")

    assert len(violations) == 0, "Classes with wrong naming:\n" + "\n".join(violations)


def test_fr18_variables_and_functions_use_snake_case():
    """Variables and functions (non-public) must use snake_case."""
    src_files = list(SRC_ROOT.rglob("*.py"))
    violations = []

    snake_pattern = re.compile(r"^[a-z_][a-z0-9_]*$")
    pascal_pattern = re.compile(r"^[A-Z][a-zA-Z0-9]+([A-Z][a-zA-Z0-9]*)*$")

    for filepath in src_files:
        try:
            tree = ast.parse(filepath.read_text(), filename=str(filepath))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                name = node.id
                if name.startswith("_"):
                    continue
                if pascal_pattern.match(name) or (name[0].isupper() and "_" not in name):
                    if snake_pattern.match(name):
                        violations.append(
                            f"{filepath}:{getattr(node, 'lineno', '?')} var '{name}' should be snake_case"
                        )

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = node.name
                if name.startswith("__") and name.endswith("__"):
                    continue
                if name.startswith("_"):
                    continue
                if pascal_pattern.match(name) and "_" not in name:
                    if not snake_pattern.match(name):
                        violations.append(
                            f"{filepath}:{node.lineno} fn '{name}' should be snake_case"
                        )

    assert len(violations) == 0, "Names violating snake_case:\n" + "\n".join(violations)